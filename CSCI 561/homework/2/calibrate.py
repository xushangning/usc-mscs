from time import process_time_ns
import pickle

from engine import Pente
from homework import minimax


REFERENCE_GAME = (
    '10K', '9M', '7K', '11K', '9H', '10L', '8N', '13H', '12J', '8J', '7H', '9K',
    '11M', '9L', '9N', '7L'
)

if __name__ == '__main__':
    game = Pente()
    for m in REFERENCE_GAME:
        game.move(m)

    depth_to_run_time = {}
    for depth in range(2, 5):
        # Run twice to eliminate cold start.
        for _ in range(2):
            start = process_time_ns()
            minimax(game, depth)
            end = process_time_ns()
            depth_to_run_time[depth] = (end - start) // 10 ** 6

    print('depth_to_run_time =', depth_to_run_time)
    with open('calibrate.txt', 'wb') as f:
        pickle.dump(depth_to_run_time, f)
