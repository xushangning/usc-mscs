import unittest

import numpy as np

from homework import a_star


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
