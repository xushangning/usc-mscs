from typing import Optional
from argparse import ArgumentParser
import json

from buildmtree import prev_pow_of_2, build, DEFAULT_TREE_FILE_NAME


def consistent(old_tree: dict[str], new_tree: dict[str]) -> Optional[list[str]]:
    if old_tree['size'] > new_tree['size']:
        return None
    if old_tree['size'] == new_tree['size']:
        return [old_tree['hash']] if old_tree['hash'] == new_tree['hash'] else None

    if (ret := consistent_recursive(old_tree, new_tree)) is not None:
        if ret[0] != old_tree['hash']:
            ret = [old_tree['hash']] + ret
        ret.append(new_tree['hash'])
    return ret


def consistent_recursive(old_tree: dict[str], new_tree: dict[str]) -> Optional[list[str]]:
    if old_tree['size'] == new_tree['size']:
        return [new_tree['hash']] if old_tree['hash'] == new_tree['hash'] else None

    k = prev_pow_of_2(new_tree['size'])
    if old_tree['size'] <= k:
        if (ret := consistent_recursive(old_tree, new_tree['left'])) is None:
            return None
        ret.append(new_tree['right']['hash'])
        return ret

    if old_tree['left']['hash'] != new_tree['left']['hash']:
        return None
    if (ret := consistent_recursive(old_tree['right'], new_tree['right'])) is None:
        return None
    ret.append(new_tree['left']['hash'])
    return ret


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('old', type=json.loads, help='a JSON array of items for the old Merkle tree')
    parser.add_argument('new', type=json.loads, help='a JSON array of items for the new Merkle tree')
    args = parser.parse_args()

    old_tree = build(tuple(s.encode('utf-8') for s in args.old))
    new_tree = build(tuple(s.encode('utf-8') for s in args.new))
    with open(DEFAULT_TREE_FILE_NAME + 's', 'w') as f:
        json.dump({'old': old_tree, 'new': new_tree}, f, indent=4)
    proof = consistent(old_tree, new_tree)
    if proof is None:
        print('No')
    else:
        print('Yes', json.dumps(proof))
