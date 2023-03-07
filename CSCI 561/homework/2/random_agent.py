from pathlib import Path
import pickle
from argparse import ArgumentParser
import random

from engine import Pente, PLAYER_STATE_FILE_NAME

NEXT_MOVE_RADIUS = 2


def play(state) -> str:
    with open('input.txt') as f:
        f_iter = iter(f)
        color = next(f_iter).rstrip('\n')
        is_white_s_turn = color == 'WHITE'
        if is_white_s_turn and state['turn'] == 0:
            return '10K'

        next(f_iter)    # skip remaining time
        next(f_iter)    # skip number of captured pairs
        pieces = {
            (Pente.BOARD_LENGTH - i - 1, j) for i in range(Pente.BOARD_LENGTH)
            for j, c in enumerate(next(f_iter).rstrip('\n')) if c != '.'
        }

    next_positions = set()
    if is_white_s_turn and state['turn'] == 1:
        # Follow the rule that alleviate the first-player advantage.
        pieces.remove((Pente.CENTER_POS, Pente.CENTER_POS))
        black_piece = next(iter(pieces))
        # The second white piece must be at least three intersections away from the first.
        next_positions.update((
            pos for pos in ((9, 12), (12, 12), (12, 9), (12, 6), (9, 6), (6, 6), (6, 9), (6, 12))
            if pos != black_piece
        ))

        bi, bj = black_piece
        for di, dj in Pente.DIRECTIONS:
            i = bi
            j = bj
            for _ in range(NEXT_MOVE_RADIUS):
                i += di
                j += dj
                if Pente.on_board(i, j) and abs(i - Pente.CENTER_POS) >= 3 and abs(j - Pente.CENTER_POS) >= 3:
                    next_positions.add((i, j))
    else:
        for i, j in pieces:
            for di, dj in Pente.DIRECTIONS:
                ti = i
                tj = j
                for _ in range(NEXT_MOVE_RADIUS):
                    ti += di
                    tj += dj
                    if Pente.on_board(ti, tj) and (ti, tj) not in pieces:
                        next_positions.add((ti, tj))

    i = random.randrange(len(next_positions))
    for j, pos in enumerate(next_positions):
        if j == i:
            return Pente.to_algebraic_notation(*pos)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()

    state_path = Path(PLAYER_STATE_FILE_NAME)
    if state_path.exists():
        with open(state_path, 'rb') as f_state:
            state = pickle.load(f_state)
            random.setstate(state['rng_state'])
    else:
        random.seed(args.seed)
        state = {'turn': 0}

    move = play(state)
    with open('output.txt', 'w') as f:
        print(move, file=f)

    state['turn'] += 1
    state['rng_state'] = random.getstate()

    with open(state_path, 'wb') as f_state:
        pickle.dump(state, f_state)
