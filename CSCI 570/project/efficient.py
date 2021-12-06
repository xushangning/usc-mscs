import numpy as np
import sys
import os
import time
import psutil
import argparse


def generate_string(input_string):
    """Read from input and return two generated sequences."""
    base_1 = input_string[0]
    for i in range(1, len(input_string)):
        if (ord(input_string[i][0]) >= 48) & (ord(input_string[i][0]) <= 57):
            base_1 = base_1[0: (int(input_string[i]) + 1)] + base_1 + base_1[(int(input_string[i]) + 1): len(base_1)]
        else:
            base_2 = input_string[i]
            break
    j = i - 1
    for i in range(j + 2, len(input_string)):
        base_2 = base_2[0: (int(input_string[i]) + 1)] + base_2 + base_2[(int(input_string[i]) + 1): len(base_2)]
    k = i - j - 1
    if (len(base_1) != 2 ** j * len(input_string[0])) | (len(base_2) != 2 ** k * len(input_string[j + 1])):
        print("String length error!")
        sys.exit(1)
    return base_1, base_2


def match_string_dp(x, y, alpha, delta):
    """Input two generated sequences, alpha and delta, and return a tuple containing the first 50 elements and the
    last 50 elements of the actual alignment(4 strings). """
    m = len(x)
    n = len(y)
    opt = np.zeros((m + 1, n + 1))
    for i in range(m + 1):
        opt[i, 0] = i * delta
    for j in range(n + 1):
        opt[0, j] = j * delta
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            x_idx = (x[i - 1] == 'A') * 0 + (x[i - 1] == 'C') * 1 + (x[i - 1] == 'G') * 2 + (x[i - 1] == 'T') * 3
            y_idx = (y[j - 1] == 'A') * 0 + (y[j - 1] == 'C') * 1 + (y[j - 1] == 'G') * 2 + (y[j - 1] == 'T') * 3
            opt[i, j] = min(opt[i - 1, j - 1] + alpha[x_idx][y_idx], opt[i - 1, j] + delta, opt[i, j - 1] + delta)
    print(opt[m, n])
    i = len(x)
    j = len(y)
    alignment_x_inv = ''
    alignment_y_inv = ''
    while (1):
        if (i == 0) & (j == 0):
            break
        elif i == 0:
            alignment_x_inv = alignment_x_inv + '_'
            alignment_y_inv = alignment_y_inv + y[j - 1]
            j = j - 1
        elif j == 0:
            alignment_x_inv = alignment_x_inv + x[i - 1]
            alignment_y_inv = alignment_y_inv + '_'
            i = i - 1
        else:
            x_idx = (x[i - 1] == 'A') * 0 + (x[i - 1] == 'C') * 1 + (x[i - 1] == 'G') * 2 + (x[i - 1] == 'T') * 3
            y_idx = (y[j - 1] == 'A') * 0 + (y[j - 1] == 'C') * 1 + (y[j - 1] == 'G') * 2 + (y[j - 1] == 'T') * 3
            if (opt[i - 1, j - 1] + alpha[x_idx][y_idx] < opt[i - 1, j] + delta) & (
                    opt[i - 1, j - 1] + alpha[x_idx][y_idx] < opt[i, j - 1] + delta):
                alignment_x_inv = alignment_x_inv + x[i - 1]
                alignment_y_inv = alignment_y_inv + y[j - 1]
                i = i - 1
                j = j - 1
            elif (opt[i - 1, j] + delta) < (opt[i, j - 1] + delta):
                alignment_x_inv = alignment_x_inv + x[i - 1]
                alignment_y_inv = alignment_y_inv + '_'
                i = i - 1
            else:
                alignment_x_inv = alignment_x_inv + '_'
                alignment_y_inv = alignment_y_inv + y[j - 1]
                j = j - 1
        alignment_x = alignment_x_inv[::-1]
        alignment_y = alignment_y_inv[::-1]
    return alignment_x, alignment_y


def match_string_dc(x, y, alpha, delta):
    """Input two generated sequences, alpha and delta, and return a tuple containing the first 50 elements and the
    last 50 elements of the actual alignment (4 strings). """
    m = len(x)
    n = len(y)
    if n <= 2 or m <= 2:
        return match_string_dp(x, y, alpha, delta)
    f = np.zeros((m + 1, 2))
    g = np.zeros((m + 1, 2))
    for i in range(m + 1):
        f[i, 0] = i * delta
    for j in range(1, n // 2 + 1):
        f[0, 1] = j * delta
        for i in range(1, m + 1):
            x_idx = (x[i - 1] == 'A') * 0 + (x[i - 1] == 'C') * 1 + (x[i - 1] == 'G') * 2 + (x[i - 1] == 'T') * 3
            y_idx = (y[j - 1] == 'A') * 0 + (y[j - 1] == 'C') * 1 + (y[j - 1] == 'G') * 2 + (y[j - 1] == 'T') * 3
            f[i, 1] = min(f[i - 1, 0] + alpha[x_idx][y_idx],
                          f[i - 1, 1] + delta,
                          f[i, 0] + delta)
        for i in range(m + 1):
            f[i, 0] = f[i, 1]
    for i in range(m + 1):
        g[i, 0] = i * delta
    for j in range(1, n - (n // 2) + 1):
        g[0, 1] = j * delta
        for i in range(1, m + 1):
            x_idx = (x[m - i] == 'A') * 0 + (x[m - i] == 'C') * 1 + (x[m - i] == 'G') * 2 + (x[m - i] == 'T') * 3
            y_idx = (y[n - j] == 'A') * 0 + (y[n - j] == 'C') * 1 + (y[n - j] == 'G') * 2 + (y[n - j] == 'T') * 3
            g[i, 1] = min(g[i - 1, 0] + alpha[x_idx][y_idx],
                          g[i - 1, 1] + delta,
                          g[i, 0] + delta)
        for i in range(m + 1):
            g[i, 0] = g[i, 1]
    q = 0
    for i in range(m + 1):
        if f[i, 0] + g[m - i, 0] < f[q, 0] + g[m - q, 0]:
            q = i
    print(f[q, 0] + g[m - q, 0])
    alignment_x1, alignment_y1 = match_string_dc(x[:q], y[:n // 2], alpha, delta)
    alignment_x2, alignment_y2 = match_string_dc(x[q:], y[n // 2:], alpha, delta)
    return alignment_x1 + alignment_x2, alignment_y1 + alignment_y2


def calc_memory():
    """Calculate the memory used."""
    pid = os.getpid()
    p = psutil.Process(pid)
    info = p.memory_full_info()
    memory = info.uss
    return memory


def test(match_string_func, input_file, output_file):
    start_time = time.process_time()
    start_memory = calc_memory()
    delta = 30
    alpha = np.array([[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]])
    input_string = np.loadtxt(input_file, dtype=str)
    base_1, base_2 = generate_string(input_string)
    alignment = match_string_func(base_1, base_2, alpha, delta)
    end_memory = calc_memory()
    memory = end_memory - start_memory
    end_time = time.process_time()
    runtime = end_time - start_time
    output = (
    alignment[0][:50] + ' ' + alignment[0][-50:], alignment[1][:50] + ' ' + alignment[1][-50:], runtime, memory)
    np.savetxt(output_file, output, fmt='%s', newline='\n')

if __name__ == '__main__':
    OUTPUT_FILE_NAME = 'output.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()
    test(match_string_func=match_string_dp, input_file=args.input_file, output_file=OUTPUT_FILE_NAME)
    test(match_string_func=match_string_dc, input_file=args.input_file, output_file=OUTPUT_FILE_NAME)
