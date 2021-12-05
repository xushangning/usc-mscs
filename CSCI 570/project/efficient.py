import numpy as np
import pandas as pd
import sys
import os
import time
import psutil


def generate_string(input_string):
    """Read from input and return two generated sequences."""
    base_1 = input_string.iloc[0, 0]
    for i in range(1, len(input_string)):
        if (ord(input_string.iloc[i, 0][0]) >= 48) & (ord(input_string.iloc[i, 0][0]) <= 57):
            base_1 = base_1[0: (int(input_string.iloc[i, 0]) + 1)] + base_1 + base_1[
                                                                              (int(input_string.iloc[i, 0]) + 1): len(
                                                                                  base_1)]
        else:
            base_2 = input_string.iloc[i, 0]
            break
    j = i - 1
    for i in range(j + 2, len(input_string)):
        base_2 = base_2[0: (int(input_string.iloc[i, 0]) + 1)] + base_2 + base_2[
                                                                          (int(input_string.iloc[i, 0]) + 1): len(
                                                                              base_2)]
    k = i - j - 1
    if (len(base_1) != 2 ** j * len(input_string.iloc[0, 0])) | (
            len(base_2) != 2 ** k * len(input_string.iloc[j + 1, 0])):
        print("String length error!")
        sys.exit(1)
    return base_1, base_2


def match_string_dp(x, y, alpha, delta):
    """Input two generated sequences, alpha and delta, and return a tuple containing the first 50 elements and the
    last 50 elements of the actual alignment(4 strings). """
    m = len(x)
    n = len(y)
    opt = np.zeros((m + 1, n + 1))
    opt = pd.DataFrame(opt)
    for i in range(m + 1):
        opt.iloc[i, 0] = i * delta
    for j in range(n + 1):
        opt.iloc[0, j] = j * delta
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            opt.iloc[i, j] = min(opt.iloc[i - 1, j - 1] + alpha[x[i - 1]][y[j - 1]],
                                 opt.iloc[i - 1, j] + delta,
                                 opt.iloc[i, j - 1] + delta)
    print(opt.iloc[m, n])
    i = m
    j = n
    alignment_x_inv = ''
    alignment_y_inv = ''
    while 1:
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
            if (opt.iloc[i - 1, j - 1] + alpha[x[i - 1]][y[j - 1]] < opt.iloc[i - 1, j] + delta) & (
                    opt.iloc[i - 1, j - 1] + alpha[x[i - 1]][y[j - 1]] < opt.iloc[i, j - 1] + delta):
                alignment_x_inv = alignment_x_inv + x[i - 1]
                alignment_y_inv = alignment_y_inv + y[j - 1]
                i = i - 1
                j = j - 1
            elif (opt.iloc[i - 1, j] + delta) < (opt.iloc[i, j - 1] + delta):
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
    last 50 elements of the actual alignment(4 strings). """
    m = len(x)
    n = len(y)
    if n <= 2 or m <= 2:
        return match_string_dp(x, y, alpha, delta)
    f = np.zeros((m + 1, 2))
    g = np.zeros((m + 1, 2))
    f = pd.DataFrame(f)
    g = pd.DataFrame(g)
    for i in range(m + 1):
        f.iloc[i, 0] = i * delta
    for j in range(1, n // 2 + 1):
        f.iloc[0, 1] = j * delta
        for i in range(1, m + 1):
            f.iloc[i, 1] = min(f.iloc[i - 1, 0] + alpha[x[i - 1]][y[j - 1]],
                               f.iloc[i - 1, 1] + delta,
                               f.iloc[i, 0] + delta)
        for i in range(m + 1):
            f.iloc[i, 0] = f.iloc[i, 1]

    for i in range(m + 1):
        g.iloc[i, 0] = i * delta
    for j in range(1, n - (n // 2) + 1):
        g.iloc[0, 1] = j * delta
        for i in range(1, m + 1):
            g.iloc[i, 1] = min(g.iloc[i - 1, 0] + alpha[x[m - i]][y[n - j]],
                               g.iloc[i - 1, 1] + delta,
                               g.iloc[i, 0] + delta)
        for i in range(m + 1):
            g.iloc[i, 0] = g.iloc[i, 1]
    q = 0
    for i in range(m + 1):
        if f.iloc[i, 0] + g.iloc[i, 0] < f.iloc[q, 0] + g.iloc[q, 0]:
            q = i
    print(f.iloc[q, 0] + g.iloc[q, 0])
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
    alpha = pd.DataFrame({'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
                          'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
                          'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
                          'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}})
    input_string = pd.read_csv(input_file, header=None)
    base_1, base_2 = generate_string(input_string)
    alignment = match_string_func(base_1, base_2, alpha, delta)
    end_memory = calc_memory()
    memory = end_memory - start_memory
    end_time = time.process_time()
    runtime = end_time - start_time
    output = (alignment[0][:50] + ' ' + alignment[0][-50:], alignment[1][:50] + ' ' + alignment[1][-50:], runtime, memory)
    output = pd.DataFrame(output)
    output.to_csv(output_file, index=False, header=False)
    # The form of output here is identical to that given by TA (see "output1.txt").


if __name__ == '__main__':
    test(match_string_func=match_string_dp, input_file="input2.txt", output_file="output2_dp.txt")
    test(match_string_func=match_string_dp, input_file="input2.txt", output_file="output2_dc.txt")
