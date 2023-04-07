import random
from argparse import ArgumentParser
import secrets
import json


def generate_prime(size=512):
    while True:
        n = secrets.randbits(size - 2) << 1
        # Avoid even numbers.
        n |= 1 | 1 << (size - 1)
        if miller_rabin(n):
            return n


def witness(a: int, n: int) -> bool:
    u = n - 1
    t = 0
    while u % 2 == 0:
        u //= 2
        t += 1

    x = pow(a, u, n)
    for _ in range(t):
        x_next = x * x % n
        if x_next == 1 and x != 1 and x != n - 1:
            return True
        x = x_next
    return x != 1


def miller_rabin(n: int, n_trials=100) -> bool:
    for _ in range(n_trials):
        a = random.randrange(1, n)
        if witness(a, n):
            return False
    return True


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('name')
    args = parser.parse_args()

    p = generate_prime()
    q = generate_prime()
    e = 65537
    n = p * q
    totient = n - p - q + 1
    d = pow(e, -1, totient)

    with open(args.name + '.pub', 'w') as f:
        json.dump({'e': e, 'n': n}, f)
    with open(args.name + '.prv', 'w') as f:
        json.dump({'d': d, 'n': n}, f)
