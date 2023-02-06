from enum import IntEnum
from collections import deque
from typing import Optional, Dict, Tuple, Iterable
import typing
from heapq import heappop, heappush
from argparse import ArgumentParser

import numpy as np

__doc__ = """A few self-imposed coding conventions: Don't write a[i, j]. Write
a[y, x] instead to constantly remind myself of the mapping between 2D
coordinates and array indices: coordinate (x, y) corresponds to a[y, x].

Python 3.7.5 compatibility issues: tuple, dict and types from collections.abc
can't be used in type annotation. Their counterparts in typing like Tuple must
be used instead."""

ACTIONS = np.array(
    ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)),
    dtype='int32'
)


class Action(IntEnum):
    """Naming convention: <y-offset>_<x-offset>"""
    START = -1
    NONE = 0
    ZERO_POS = 1
    POS_POS = 2
    POS_ZERO = 3
    POS_NEG = 4
    ZERO_NEG = 5
    NEG_NEG = 6
    NEG_ZERO = 7
    NEG_POS = 8


def can_ski(current: int, successor: int, stamina: int, momentum: int) -> bool:
    # We may be standing atop a tree, which is denoted by negative elevation!
    current = abs(current)
    return current >= abs(successor) or (0 <= successor <= current + stamina + momentum)


Path = Iterable[Tuple[int, int]]


def reconstruct_path(
    start: Tuple[int, int], lodge2cost: Dict[Tuple[int, int], Optional[int]], predecessor: np.ndarray
) -> Iterable[Optional[Tuple[int, Path]]]:
    for v_tuple, cost in lodge2cost.items():
        if cost is None:
            yield None
            continue

        v = np.array(v_tuple, dtype='int32')
        reversed_action_path = []
        while True:
            reversed_action_path.append(v_tuple)
            if v_tuple == start:
                break
            v -= ACTIONS[predecessor[v_tuple] - 1]
            v_tuple = tuple(v)
        yield cost, reversed(reversed_action_path)


def bfs(
    terrain: np.ndarray, start: np.ndarray, lodges: np.ndarray, stamina: int
) -> Iterable[Optional[Tuple[int, Path]]]:
    lodge2cost = dict.fromkeys(map(tuple, lodges))
    n_lodges_done = 0

    predecessor = np.zeros_like(terrain, dtype='int8')
    start_tuple = tuple(start)
    predecessor[start_tuple] = Action.START
    frontier = deque((start,))
    level = 1
    while frontier:
        for _ in range(len(frontier)):
            current = frontier.popleft()
            current_tuple = tuple(current)

            for direction, action in enumerate(ACTIONS, 1):
                successor = current + action
                if 0 <= successor[0] < terrain.shape[0] and 0 <= successor[1] < terrain.shape[1]:
                    successor_tuple = tuple(successor)
                    if (predecessor[successor_tuple] == Action.NONE
                            and can_ski(terrain[current_tuple], terrain[successor_tuple], stamina, 0)):
                        frontier.append(successor)
                        predecessor[successor_tuple] = direction

                        if successor_tuple in lodge2cost:
                            lodge2cost[successor_tuple] = level
                            n_lodges_done += 1
            if n_lodges_done == lodges.shape[0]:
                break
        level += 1

    return reconstruct_path(start_tuple, lodge2cost, predecessor)


def ucs(
    terrain: np.ndarray, start: np.ndarray, lodges: np.ndarray, stamina: int
) -> Iterable[Optional[Tuple[int, Path]]]:
    lodge2cost = dict.fromkeys(map(tuple, lodges))
    n_lodges_done = 0

    predecessor = np.zeros_like(terrain, dtype='int8')
    start_tuple = tuple(start)
    frontier = [(0, start_tuple, Action.START)]
    while frontier:
        cost, current_tuple, pred = heappop(frontier)

        if predecessor[current_tuple] == Action.NONE:
            predecessor[current_tuple] = pred
        else:
            continue

        if current_tuple in lodge2cost:
            lodge2cost[current_tuple] = cost
            n_lodges_done += 1
            if n_lodges_done == lodges.shape[0]:
                break

        current = np.array(current_tuple, dtype='int32')
        for direction, action in enumerate(ACTIONS, 1):
            successor = current + typing.cast(np.ndarray, action)
            if 0 <= successor[0] < terrain.shape[0] and 0 <= successor[1] < terrain.shape[1]:
                successor_tuple = tuple(successor)
                if (predecessor[successor_tuple] == Action.NONE
                        and can_ski(terrain[current_tuple], terrain[successor_tuple], stamina, 0)):
                    successor_cost = cost + (14 if action[0] and action[1] else 10)
                    heappush(frontier, (successor_cost, successor_tuple, typing.cast(Action, direction)))

    return reconstruct_path(start_tuple, lodge2cost, predecessor)


def heuristic(n: np.ndarray, n_elevation: int, goal: np.ndarray, goal_elevation: int) -> int:
    """The heuristic is the sum of a diagonal distance and elevation difference
    between n and the goal state. The distance is the minimum cost of a path
    that can extend horizontally, vertically or 45-degree diagonally.

    n_elevation and goal_elevation can't be negative."""
    sides = abs(n - goal)
    return max(sides) * 14 + abs(sides[0] - sides[1]) * 10 + max(0, goal_elevation - abs(n_elevation))


def a_star(
    terrain: np.ndarray, start: np.ndarray, lodges: np.ndarray, stamina: int
) -> Iterable[Optional[Tuple[int, Path]]]:
    # A state's predecessor in A* is now represented by its previous action and
    # the predecessor's momentum.
    Predecessor = Tuple[Action, int]

    # Lodge -> Predecessor
    lodge_predecessor: Dict[Tuple[int, int], Optional[Predecessor]] = dict(
        (tuple(lodge), None) for lodge in lodges
    )

    for lodge_tuple in lodge_predecessor:
        lodge = np.array(lodge_tuple, dtype='int32')
        lodge_elevation = terrain[lodge_tuple]

        predecessor: Dict[Tuple[Tuple[int, int], int], Predecessor] = {}
        start_state: Tuple[Tuple[int, int], int] = (tuple(start), 0)
        frontier = [(0, start_state, (Action.START, 0))]
        cost_action_path: Optional[Tuple[int, Path]] = None
        while frontier:
            cost, current_state, pred = heappop(frontier)

            if current_state in predecessor:
                continue
            else:
                predecessor[current_state] = pred

            current_tuple, momentum = current_state
            current = np.array(current_tuple, dtype='int32')
            if current_tuple == lodge_tuple:
                reversed_action_path = []
                while True:
                    reversed_action_path.append(current_state[0])
                    if current_state == start_state:
                        break

                    action, momentum = predecessor[current_state]
                    current -= ACTIONS[action - 1]
                    current_state = (tuple(current), momentum)
                cost_action_path = cost, reversed(reversed_action_path)
                break

            current_elevation = abs(terrain[current_tuple])
            current_path_cost = cost - heuristic(current, current_elevation, lodge, lodge_elevation)
            for direction, action in enumerate(ACTIONS, 1):
                successor = current + typing.cast(np.ndarray, action)
                if 0 <= successor[0] < terrain.shape[0] and 0 <= successor[1] < terrain.shape[1]:
                    successor_tuple = tuple(successor)
                    successor_elevation = terrain[successor_tuple]
                    successor_elevation_abs = abs(successor_elevation)
                    successor_momentum = max(0, current_elevation - successor_elevation_abs)
                    successor_state = (successor_tuple, successor_momentum)
                    if (successor_state not in predecessor
                            and can_ski(current_elevation, successor_elevation, stamina, successor_momentum)):
                        successor_cost = current_path_cost\
                            + (14 if action[0] and action[1] else 10)\
                            + heuristic(successor, successor_elevation_abs, lodge, lodge_elevation)
                        heappush(
                            frontier,
                            (
                                successor_cost,
                                successor_state,
                                (typing.cast(Action, direction), momentum)
                            )
                        )
        yield cost_action_path


ALGORITHMS = {'BFS': bfs, 'UCS': ucs, 'A*': a_star}

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--print-cost', action='store_true')
    args = parser.parse_args()

    with open('input.txt', 'r') as f_in:
        f_iter = iter(f_in)
        algorithm = next(f_iter).rstrip('\n')
        next(f_iter)    # Ignore width and height.
        start = np.fromstring(next(f_iter).rstrip('\n'), dtype='int32', sep=' ')
        stamina = int(next(f_iter).rstrip('\n'))
        n_lodges = int(next(f_iter).rstrip('\n'))

        lodges = np.loadtxt(f_iter, max_rows=n_lodges, ndmin=2, dtype='int32')
        terrain = np.loadtxt(f_iter, ndmin=2, dtype='int32')

    # Switch order of indices because (x, y) corresponds to a[y, x].
    start[0], start[1] = start[1], start[0]
    for coordinate in lodges:
        coordinate[0], coordinate[1] = coordinate[1], coordinate[0]

    with open('output.txt', 'w') as f_out:
        for cost_path in ALGORITHMS[algorithm](terrain, start, lodges, stamina):
            s = 'FAIL'
            if cost_path is not None:
                cost, path = cost_path
                s = ''
                if args.print_cost:
                    s += str(cost) + ' '
                s += ' '.join(f'{x},{y}' for y, x in path)
            print(s, file=f_out)
