import numpy as np
import random
import matplotlib.pyplot as plt
import time

BOARD_ROWS = 5
BOARD_COLS = 5
START = (0, 0)
WIN_STATE = (4, 4)
HOLE_STATE = [(1, 0), (3, 1), (4, 2), (1, 3)]


class State:
    def __init__(self, state=START):
        self.state = state
        self.isEnd = False

    def getReward(self):
        if self.state == WIN_STATE:
            return 1
        elif self.state in HOLE_STATE:
            return -5
        else:
            return -1

    def isEndFunc(self):
        if self.state == WIN_STATE or self.state in HOLE_STATE:
            self.isEnd = True

    def nxtPosition(self, action):
        if action == 0:
            nxtState = (self.state[0] - 1, self.state[1])  # up
        elif action == 1:
            nxtState = (self.state[0] + 1, self.state[1])  # down
        elif action == 2:
            nxtState = (self.state[0], self.state[1] - 1)  # left
        else:
            nxtState = (self.state[0], self.state[1] + 1)  # right

        if 0 <= nxtState[0] <= 4 and 0 <= nxtState[1] <= 4:
            return nxtState
        return self.state


class Agent:
    def __init__(self):
        self.actions = [0, 1, 2, 3]
        self.Q = {}
        self.new_Q = {}
        self.plot_reward = []
        self.alpha = 0.5
        self.gamma = 0.9
        self.epsilon = 0.1

        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                for k in range(len(self.actions)):
                    self.Q[(i, j, k)] = 0
                    self.new_Q[(i, j, k)] = 0

    def Action(self, State):
        rnd = random.random()
        i, j = State.state
        if rnd > self.epsilon:
            max_q = -float('inf')
            best_action = 0
            for a in self.actions:
                if self.Q[(i, j, a)] > max_q:
                    max_q = self.Q[(i, j, a)]
                    best_action = a
            return State.nxtPosition(best_action), best_action
        else:
            a = random.choice(self.actions)
            return State.nxtPosition(a), a

    def Q_Learning(self, episodes):
        rewards = 0
        self.plot_reward = []
        self.new_Q = self.Q.copy()

        for _ in range(episodes):
            state = State()
            state.isEndFunc()
            while not state.isEnd:
                next_state, action = self.Action(state)
                i, j = state.state
                reward = state.getReward()
                rewards += reward

                max_q_next = max([self.Q[(next_state[0], next_state[1], a)] for a in self.actions])
                q_val = (1 - self.alpha) * self.Q[(i, j, action)] + self.alpha * (reward + self.gamma * max_q_next)
                self.new_Q[(i, j, action)] = round(q_val, 3)

                state = State(next_state)
                state.isEndFunc()

            self.Q = self.new_Q.copy()
            self.plot_reward.append(rewards)
            rewards = 0

    def run_benchmark(self, episode_list):
        results = []
        for episodes in episode_list:
            print(f"Training for {episodes} episodes...")
            start_time = time.time()
            self.Q_Learning(episodes)
            end_time = time.time()
            exec_time = end_time - start_time
            results.append((episodes, exec_time))
            print(f"Time taken: {exec_time:.4f} seconds\n")
        return results


if __name__ == "__main__":
    ag = Agent()
    episode_sizes = [1000, 5000, 10000]
    cpu_times = ag.run_benchmark(episode_sizes)

    # Save benchmark results to a file
    with open("cpu_time_log.txt", "w") as f:
        for ep, t in cpu_times:
            f.write(f"{ep},{t:.6f}\n")
    print("Execution times written to cpu_time_log.txt.")
