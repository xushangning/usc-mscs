from typing import Optional
from argparse import ArgumentParser
import json
from hashlib import sha256

from buildmtree import DEFAULT_TREE_FILE_NAME


def include(digest: str, tree: dict[str]) -> Optional[list[str]]:
    if tree['size'] == 1:
        return [] if tree['hash'] == digest else None

    if (ret := include(digest, tree['left'])) is not None:
        ret.append(tree['right']['hash'])
        return ret
    if (ret := include(digest, tree['right'])) is not None:
        ret.append(tree['left']['hash'])
        return ret
    return None


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('item')
    args = parser.parse_args()

    with open(DEFAULT_TREE_FILE_NAME) as f:
        tree = json.load(f)
    proof = include(sha256(args.item.encode('utf-8')).hexdigest(), tree)
    if proof is None:
        print('No')
    else:
        print('Yes', json.dumps(proof))
