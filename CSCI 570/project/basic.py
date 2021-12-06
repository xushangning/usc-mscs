import numpy as np
import pandas as pd
import sys
import os
import time
import psutil
import argparse

def generate_string(input):
    """Read from input and return two generated sequences."""
    base_1 = input.iloc[0, 0]
    for i in range(1, len(input)):
        if (ord(input.iloc[i, 0][0]) >= 48) & (ord(input.iloc[i, 0][0]) <= 57):
            base_1 = base_1[0: (int(input.iloc[i, 0]) + 1)] + base_1 + base_1[(int(input.iloc[i, 0]) + 1): len(base_1)]
        else:
            base_2 = input.iloc[i, 0]
            break
    j = i - 1
    for i in range(j + 2, len(input)):
        base_2 = base_2[0: (int(input.iloc[i, 0]) + 1)] + base_2 + base_2[(int(input.iloc[i, 0]) + 1): len(base_2)]
    k = i - j - 1
    if (len(base_1) != 2 ** j * len(input.iloc[0, 0])) | (len(base_2) != 2 ** k * len(input.iloc[j + 1, 0])):
        print("String length error!")
        sys.exit(1)
    return base_1,base_2

def match_string(x, y, alpha, delta) :
    """Input two generated sequences, alpha and delta, and return a tuple containing the first 50 elements and the last 50 elements of the actual alignment(4 strings)."""
    opt = np.zeros((len(x) + 1, len(y) + 1))
    opt = pd.DataFrame(opt)
    for i in range(opt.shape[0]):
        opt.iloc[i, 0] = i * delta
    for j in range(opt.shape[1]):
        opt.iloc[0, j] = j * delta
    for j in range(1, opt.shape[1]):
        for i in range(1, opt.shape[0]):
            opt.iloc[i, j] = min(opt.iloc[i - 1, j - 1] + alpha[x[i - 1]][y[j - 1]], opt.iloc[i - 1, j] + delta, opt.iloc[i, j - 1] + delta)
    i = len(x)
    j = len(y)
    alignment_x_inv = ''
    alignment_y_inv = ''
    while(1):
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
            if (opt.iloc[i - 1, j - 1] + alpha[x[i - 1]][y[j - 1]] < opt.iloc[i - 1, j] + delta) & (opt.iloc[i - 1, j - 1] + alpha[x[i - 1]][y[j - 1]] < opt.iloc[i, j - 1] + delta):
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
    return (alignment_x[0:50], alignment_x[-50:], alignment_y[0:50], alignment_y[-50:])

def calc_memory():
    '''Calculate the memory used.'''
    pid = os.getpid()
    p = psutil.Process(pid)
    info = p.memory_full_info()
    memory = info.uss
    return memory

def main():
    OUTPUT_FILE_NAME = 'output.txt'
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()

    start_time = time.process_time()
    start_memory = calc_memory()
    delta = 30
    alpha = pd.DataFrame({'A': {'A': 0, 'C': 110, 'G': 48, 'T': 94},
                          'C': {'A': 110, 'C': 0, 'G': 118, 'T': 48},
                          'G': {'A': 48, 'C': 118, 'G': 0, 'T': 110},
                          'T': {'A': 94, 'C': 48, 'G': 110, 'T': 0}})
    input = pd.read_csv(args.input_file, header=None)
    base_1, base_2 = generate_string(input)
    alignment = match_string(base_1, base_2, alpha, delta)
    end_memory = calc_memory()
    memory = end_memory - start_memory
    end_time = time.process_time()
    runtime = end_time - start_time
    output = (alignment[0] + ' ' + alignment[1], alignment[2] + ' ' + alignment[3], runtime, memory)
    output = pd.DataFrame(output)
    output.to_csv(OUTPUT_FILE_NAME, index=0, header=0) #The form of output here is identical to that given by TA (see "output1.txt").

if __name__ == '__main__':
    main()
