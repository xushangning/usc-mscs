from argparse import ArgumentParser
from pathlib import Path

import numpy as np

parser = ArgumentParser()
parser.add_argument('--preset', choices=('small', 'full'), default='small')
args = parser.parse_args()

TEST_CASES_PER_ALGO = 10
INT32_MAX = 2 ** 31 - 1
INT32_MIN = - 2 ** 31

shape_max = 16
elevation_range = -128, 127
if args.preset == 'full':
    shape_max = 500
    elevation_range = INT32_MIN, INT32_MAX

rng = np.random.default_rng(0)

directory = Path('test_cases')
directory.mkdir(exist_ok=True)

i = 0
for algo in 'BFS', 'UCS', 'A*':
    for _ in range(TEST_CASES_PER_ALGO):
        # Avoid a shape of (1, 1).
        shape = np.divmod(rng.integers(1, shape_max * shape_max), shape_max)
        shape = shape[0] + 1, shape[1] + 1

        terrain = rng.integers(*elevation_range, size=shape, dtype='int32')

        size = shape[0] * shape[1]
        n_lodges = rng.integers(1, max(shape))
        start_and_lodges = np.stack(
            np.divmod(rng.choice(size, size=n_lodges + 1, replace=False, shuffle=False), shape[1]),
            axis=1
        )
        for y, x in start_and_lodges:
            # Remove trees from the locations of the starting point and lodges
            # by setting elevation to a non-negative value.
            terrain[y, x] = abs(terrain[y, x])

        stamina = rng.integers(elevation_range[1])

        with (directory / f'input{i}.txt').open('w') as f:
            print(algo, file=f)
            print(*reversed(shape), file=f)
            print(*reversed(start_and_lodges[0]), file=f)
            print(stamina, file=f)
            print(n_lodges, file=f)

            for lodge in start_and_lodges[1:]:
                print(*reversed(lodge), file=f)

            for row in terrain:
                print(' '.join(map(str, row)), file=f)

        i += 1

# probably should use or linspace for shapes. shouldn't really use purely
# random sizes, because i want to test the worst case, or that i want to test
# it thoroughly and cover a variety of shapes.
