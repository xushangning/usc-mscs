from collections.abc import Sequence
from hashlib import sha256
from argparse import ArgumentParser
import json

DEFAULT_TREE_FILE_NAME = 'merkle.tree'


def prev_pow_of_2(n: int) -> int:
    """Return the largest power of 2 less than n."""
    return 2 ** ((n - 1).bit_length() - 1)


def build(data: Sequence[bytes]) -> dict[str]:
    if len(data) == 1:
        return {'hash': sha256(data[0]).hexdigest(), 'size': 1}

    k = prev_pow_of_2(len(data))
    left = build(data[:k])
    right = build(data[k:])
    return {
        'hash': sha256(bytes.fromhex(left['hash']) + bytes.fromhex(right['hash'])).hexdigest(),
        'size': len(data),
        'left': left,
        'right': right,
    }


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('item', nargs='+')
    args = parser.parse_args()
    with open(DEFAULT_TREE_FILE_NAME, 'w') as f:
        json.dump(build(tuple(s.encode('utf-8') for s in args.item)), f, indent=4)
