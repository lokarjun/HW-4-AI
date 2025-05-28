
def truncate(x):
    return x & 0xFFFFFFFF

def rotl(x, n):
    return truncate((x << n) | (x >> (32 - n)))

def quarter_round(a, b, c, d):
    a = truncate(a + b); d = rotl(d ^ a, 16)
    c = truncate(c + d); b = rotl(b ^ c, 12)
    a = truncate(a + b); d = rotl(d ^ a, 8)
    c = truncate(c + d); b = rotl(b ^ c, 7)
    return a, b, c, d

def chacha_block(input_state):
    if len(input_state) != 16:
        raise ValueError('Input must have 16 words!')
    x = input_state[:]
    for _ in range(10):  # 20 rounds: 10 column + 10 diagonal
        x[0], x[4], x[8], x[12] = quarter_round(x[0], x[4], x[8], x[12])
        x[1], x[5], x[9], x[13] = quarter_round(x[1], x[5], x[9], x[13])
        x[2], x[6], x[10], x[14] = quarter_round(x[2], x[6], x[10], x[14])
        x[3], x[7], x[11], x[15] = quarter_round(x[3], x[7], x[11], x[15])

        x[0], x[5], x[10], x[15] = quarter_round(x[0], x[5], x[10], x[15])
        x[1], x[6], x[11], x[12] = quarter_round(x[1], x[6], x[11], x[12])
        x[2], x[7], x[8], x[13] = quarter_round(x[2], x[7], x[8], x[13])
        x[3], x[4], x[9], x[14] = quarter_round(x[3], x[4], x[9], x[14])
    return x
