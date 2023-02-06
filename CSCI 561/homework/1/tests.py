from collections.abc import Iterator
from typing import Optional
from heapq import heappush, heappop
import typing
import unittest

import numpy as np

from homework import Action, ACTIONS, can_ski, elevation_change_cost, a_star


def ucs_momentum(
    terrain: np.ndarray, start: np.ndarray, lodges: np.ndarray, stamina: int
) -> Iterator[Optional[int]]:
    """UCS for cross validation with A* on large test cases. Although
    predecessor information is saved, optimal paths are currently
    not reconstructed."""
    lodge2cost = dict.fromkeys(map(tuple, lodges))
    n_lodges_done = 0

    Predecessor = tuple[Action, int]
    predecessor: dict[tuple[tuple[int, int], int], Predecessor] = {}
    start_state: tuple[tuple[int, int], int] = (tuple(start), 0)
    frontier = [(0, start_state, (Action.START, 0))]
    while frontier:
        cost, current_state, pred = heappop(frontier)

        if current_state in predecessor:
            continue
        else:
            predecessor[current_state] = pred

        current_tuple, momentum = current_state
        if current_tuple in lodge2cost and lodge2cost[current_tuple] is None:
            lodge2cost[current_tuple] = cost
            n_lodges_done += 1
            if n_lodges_done == lodges.shape[0]:
                break

        current = np.array(current_tuple, dtype='int32')
        current_elevation = abs(terrain[current_tuple])
        for direction, action in enumerate(ACTIONS, 1):
            successor = current + typing.cast(np.ndarray, action)
            if 0 <= successor[0] < terrain.shape[0] and 0 <= successor[1] < terrain.shape[1]:
                successor_tuple = tuple(successor)
                successor_elevation = terrain[successor_tuple]
                successor_elevation_abs = abs(successor_elevation)
                successor_momentum = max(0, current_elevation - successor_elevation_abs)
                successor_state = (successor_tuple, successor_momentum)
                if (successor_state not in predecessor
                        and can_ski(current_elevation, successor_elevation, stamina, momentum)):
                    successor_cost = cost\
                        + (14 if action[0] and action[1] else 10)\
                        + elevation_change_cost(current_elevation, successor_elevation_abs, momentum)
                    heappush(
                        frontier,
                        (successor_cost, successor_state, (typing.cast(Action, direction), momentum))
                    )
    return iter(lodge2cost.values())


class AStarTestCase(unittest.TestCase):
    def test_cycles(self):
        cost_path = next(a_star(
            np.array(
                (
                    (100, 100, 22, 20, 18),
                    (100, 100, 24, 100, 16),
                    (10, 10, 0, 12, 14),
                    (100, 100, 26, 100, 100),
                    (100, 100, 28, 100, 100),
                ),
                dtype='int32'
            ),
            np.array((2, 0), dtype='int32'),
            np.array(((4, 2),), dtype='int32'),
            2
        ))
        self.assertIsNotNone(cost_path)
        self.assertEqual(138, cost_path[0])


if __name__ == '__main__':
    unittest.main()
