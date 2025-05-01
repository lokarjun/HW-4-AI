%%writefile q_learning_grid.cu
#include <iostream>
#include <fstream>
#include <curand_kernel.h>

#define BOARD_ROWS 5
#define BOARD_COLS 5
#define ACTIONS 4
#define NUM_SIZES 3

// Reward constants
#define REWARD_WIN 1
#define REWARD_HOLE -5
#define REWARD_DEFAULT -1

__device__ int holes[][2] = {{1,0},{3,1},{4,2},{1,3}};
__device__ bool isHole(int x, int y) {
    for (int i = 0; i < 4; i++) {
        if (holes[i][0] == x && holes[i][1] == y) return true;
    }
    return false;
}

__device__ int getReward(int x, int y) {
    if (x == 4 && y == 4) return REWARD_WIN;
    if (isHole(x, y)) return REWARD_HOLE;
    return REWARD_DEFAULT;
}

__global__ void setupKernel(curandState *state) {
    int id = threadIdx.x;
    curand_init(1234, id, 0, &state[id]);
}

__global__ void q_learning(float *Q, curandState *globalState, int EPISODES) {
    int tid = threadIdx.x;
    if (tid != 0) return;

    curandState localState = globalState[tid];
    float alpha = 0.5f, gamma = 0.9f, epsilon = 0.1f;

    for (int ep = 0; ep < EPISODES; ep++) {
        int x = 0, y = 0;
        bool isEnd = false;

        while (!isEnd) {
            int action;
            float r = curand_uniform(&localState);
            if (r < epsilon) {
                action = curand(&localState) % ACTIONS;
            } else {
                float maxQ = -1e9;
                for (int a = 0; a < ACTIONS; a++) {
                    float q = Q[(x * BOARD_COLS + y) * ACTIONS + a];
                    if (q > maxQ) {
                        maxQ = q;
                        action = a;
                    }
                }
            }

            int new_x = x, new_y = y;
            if (action == 0 && x > 0) new_x--;
            else if (action == 1 && x < BOARD_ROWS - 1) new_x++;
            else if (action == 2 && y > 0) new_y--;
            else if (action == 3 && y < BOARD_COLS - 1) new_y++;

            int reward = getReward(new_x, new_y);
            bool done = (new_x == 4 && new_y == 4) || isHole(new_x, new_y);

            float maxQNext = -1e9;
            for (int a = 0; a < ACTIONS; a++) {
                float q = Q[(new_x * BOARD_COLS + new_y) * ACTIONS + a];
                if (q > maxQNext) maxQNext = q;
            }

            int idx = (x * BOARD_COLS + y) * ACTIONS + action;
            Q[idx] = (1 - alpha) * Q[idx] + alpha * (reward + gamma * maxQNext);

            x = new_x;
            y = new_y;
            isEnd = done;
        }
    }

    globalState[tid] = localState;
}

int main() {
    int episode_sizes[NUM_SIZES] = {1000, 5000, 10000};

    std::ofstream logFile("gpu_time_log.txt");

    for (int test = 0; test < NUM_SIZES; test++) {
        int EPISODES = episode_sizes[test];

        float *d_Q;
        curandState *devStates;
        size_t size = BOARD_ROWS * BOARD_COLS * ACTIONS * sizeof(float);

        cudaMalloc((void**)&d_Q, size);
        cudaMemset(d_Q, 0, size);
        cudaMalloc((void**)&devStates, sizeof(curandState));

        setupKernel<<<1, 1>>>(devStates);
        cudaDeviceSynchronize();

        cudaEvent_t start, stop;
        cudaEventCreate(&start);
        cudaEventCreate(&stop);
        cudaEventRecord(start);

        q_learning<<<1, 1>>>(d_Q, devStates, EPISODES);
        cudaDeviceSynchronize();

        cudaEventRecord(stop);
        cudaEventSynchronize(stop);
        float ms = 0;
        cudaEventElapsedTime(&ms, start, stop);

        std::cout << "Episodes: " << EPISODES << ", Time: " << ms / 1000.0f << " seconds\n";
        logFile << EPISODES << "," << ms / 1000.0f << "\n";

        cudaFree(d_Q);
        cudaFree(devStates);
    }

    logFile.close();
    return 0;
}
