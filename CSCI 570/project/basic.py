import numpy as np
import sys
import os
import time
import psutil
import argparse


def generate_string(input):
    """Read from input and return two generated sequences."""
    base_1 = input[0]
    for i in range(1, len(input)):
        if (ord(input[i][0]) >= 48) & (ord(input[i][0]) <= 57):
            base_1 = base_1[0: (int(input[i]) + 1)] + base_1 + base_1[(int(input[i]) + 1): len(base_1)]
        else:
            base_2 = input[i]
            break
    j = i - 1
    for i in range(j + 2, len(input)):
        base_2 = base_2[0: (int(input[i]) + 1)] + base_2 + base_2[(int(input[i]) + 1): len(base_2)]
    k = i - j - 1
    if (len(base_1) != 2 ** j * len(input[0])) | (len(base_2) != 2 ** k * len(input[j + 1])):
        print("String length error!")
        sys.exit(1)
    return base_1, base_2


def match_string(x, y, alpha, delta) :
    """Input two generated sequences, alpha and delta, and return a tuple containing the first 50 elements and the last 50 elements of the actual alignment(4 strings)."""
    opt = np.zeros((len(x) + 1, len(y) + 1))
    for i in range(opt.shape[0]):
        opt[i, 0] = i * delta
    for j in range(opt.shape[1]):
        opt[0, j] = j * delta
    for j in range(1, opt.shape[1]):
        for i in range(1, opt.shape[0]):
            x_idx = (x[i - 1] == 'A') * 0 + (x[i - 1] == 'C') * 1 + (x[i - 1] == 'G') * 2 + (x[i - 1] == 'T') * 3
            y_idx = (y[j - 1] == 'A') * 0 + (y[j - 1] == 'C') * 1 + (y[j - 1] == 'G') * 2 + (y[j - 1] == 'T') * 3
            opt[i, j] = min(opt[i - 1, j - 1] + alpha[x_idx][y_idx], opt[i - 1, j] + delta, opt[i, j - 1] + delta)
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
    return (alignment_x[0:50], alignment_x[-50:], alignment_y[0:50], alignment_y[-50:]), opt[len(x), len(y)]


def calc_memory():
    '''Calculate the memory used.'''
    pid = os.getpid()
    p = psutil.Process(pid)
    info = p.memory_full_info()
    memory = info.uss / 1000
    return memory

def main():
    OUTPUT_FILE_NAME = 'output.txt'
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()

    start_time = time.process_time()
    start_memory = calc_memory()
    delta = 30
    alpha = np.array([[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]])
    input = np.loadtxt(args.input_file, dtype=str)
    base_1, base_2 = generate_string(input)
    alignment, cost = match_string(base_1, base_2, alpha, delta)
    end_memory = calc_memory()
    memory = end_memory - start_memory
    end_time = time.process_time()
    runtime = end_time - start_time
    output = (alignment[0] + ' ' + alignment[1], alignment[2] + ' ' + alignment[3], cost, runtime, memory)
    output = np.array(output)
    np.savetxt(OUTPUT_FILE_NAME, output, fmt='%s', newline='\n')

if __name__ == '__main__':
    main()
