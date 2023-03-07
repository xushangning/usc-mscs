from typing import Optional
from argparse import ArgumentParser
from pathlib import Path
import subprocess


class Pente:
    State = tuple[list[Optional[bool]], ...]

    BOARD_LENGTH = 19
    CENTER_POS = 9
    COLUMN_HEADERS = 'ABCDEFGHJKLMNOPQRST'
    AXES = (1, 0), (0, 1), (1, 1), (-1, 1)
    DIRECTIONS = (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)
    N_PIECES_WIN = N_CAPTURES_WIN = 5
    MAX_UTILITY = 1000
    NEXT_MOVE_RADIUS = 2

    def __init__(self):
        self.result: Optional[bool] = None
        self.is_white_s_turn = True

        self._state: Pente.State = tuple(
            [None] * self.BOARD_LENGTH for _ in range(self.BOARD_LENGTH)
        )
        self.turn = 0
        self.pairs_captured = [0, 0]

    @classmethod
    def on_board(cls, i: int, j: int) -> bool:
        return 0 <= i < cls.BOARD_LENGTH and 0 <= j < cls.BOARD_LENGTH

    def _count_same_color_pieces(self, i: int, j: int, di: int, dj: int) -> int:
        current_player = self._state[i][j]
        retval = 0
        for _ in range(self.N_PIECES_WIN - 1):
            i += di
            j += dj
            if self.on_board(i, j) and self._state[i][j] is current_player:
                retval += 1
            else:
                break
        return retval

    def _capture(self, i: int, j: int, di: int, dj: int) -> bool:
        third_i = i + 3 * di
        third_j = j + 3 * dj
        if self.on_board(third_i, third_j) and self._state[third_i][third_j] is self._state[i][j]:
            first_i = i + di
            first_j = j + dj
            second_i = i + 2 * di
            second_j = j + 2 * dj
            opponent = not self._state[i][j]
            if (self._state[first_i][first_j] is opponent
                    and self._state[second_i][second_j] is opponent):
                self._state[first_i][first_j] = None
                self._state[second_i][second_j] = None
                return True
        return False

    def move(self, pos: str | tuple[int, int]):
        if isinstance(pos, str):
            i = int(pos[:-1]) - 1
            j = self.COLUMN_HEADERS.index(pos[-1])
        else:
            i, j = pos
        self._state[i][j] = self.is_white_s_turn

        player_index = int(self.is_white_s_turn)
        for di, dj in self.AXES:
            # Check five in a sequence.
            n_same_color = (1 + self._count_same_color_pieces(i, j, di, dj)
                            + self._count_same_color_pieces(i, j, -di, -dj))
            if n_same_color >= self.N_PIECES_WIN:
                self.result = self.is_white_s_turn
                break

            # Process captures.
            if self._capture(i, j, di, dj):
                self.pairs_captured[player_index] += 1
            if self._capture(i, j, -di, -dj):
                self.pairs_captured[player_index] += 1
            if self.pairs_captured[player_index] >= self.N_CAPTURES_WIN:
                self.result = self.is_white_s_turn
                break

        if not self.is_white_s_turn:
            self.turn += 1

        self.is_white_s_turn = not self.is_white_s_turn

    def __str__(self):
        """Serialize the board state according to the format in the homework."""
        retval = ''
        for row in reversed(self._state):
            retval += ''.join(
                '.' if piece is None else 'w' if piece else 'b' for piece in row
            ) + '\n'
        return retval

    def print(self):
        """Pretty print for readability."""
        print('Captures: W', self.pairs_captured[1], self.pairs_captured[0], 'B')

        print('  ', ' '.join(self.COLUMN_HEADERS))
        for i, row in enumerate(reversed(self._state)):
            print(format(self.BOARD_LENGTH - i, '2d'), end=' ')
            print(' '.join(
                '.' if piece is None else 'w' if piece else 'b' for piece in row
            ))
        # Numeric column headers for debugging with numeric coordinates.
        print(' ', ''.join(format(i, '2d') for i in range(self.BOARD_LENGTH)))

    def evaluate(self):
        shape_score = 0
        for i, row in enumerate(self._state):
            for j, piece in enumerate(row):
                if piece is None:
                    continue

                for di, dj in self.AXES:
                    streak_length = 1
                    surrounding_positions = 0
                    ti = i
                    tj = j
                    for _ in range(self.N_PIECES_WIN - 1):
                        ti += di
                        tj += dj
                        if self.on_board(ti, tj) and self._state[ti][tj] is piece:
                            streak_length += 1
                        else:
                            break
                    if self.on_board(ti, tj) and self._state[ti][tj] is None:
                        surrounding_positions += 1

                    ti = i
                    tj = j
                    for _ in range(self.N_PIECES_WIN - 1):
                        ti -= di
                        tj -= dj
                        if self.on_board(ti, tj) and self._state[ti][tj] is piece:
                            streak_length += 1
                        else:
                            break
                    if self.on_board(ti, tj) and self._state[ti][tj] is None:
                        surrounding_positions += 1

                    if piece is self.is_white_s_turn:
                        if streak_length == 2:
                            shape_score += 5 * surrounding_positions
                        elif streak_length == 3:
                            shape_score += 100 * surrounding_positions
                        elif streak_length == 4:
                            shape_score += 250 * surrounding_positions
                    else:
                        if streak_length == 2:
                            if surrounding_positions == 1:
                                shape_score += 50
                            elif surrounding_positions == 2:
                                shape_score -= 10
                        elif streak_length == 3:
                            shape_score -= 80 * surrounding_positions
                        elif streak_length == 4:
                            shape_score -= 125 * surrounding_positions

        player_index = int(self.is_white_s_turn)
        capture_score = self.pairs_captured[player_index] - self.pairs_captured[1 - player_index]
        retval = shape_score + (self.MAX_UTILITY - shape_score) * capture_score // self.N_CAPTURES_WIN

        if retval > self.MAX_UTILITY:
            retval = self.MAX_UTILITY
        if not self.is_white_s_turn:
            retval = -retval
        return retval

    def next_moves(self):
        generated_moves = set()
        for i, row in enumerate(self._state):
            for j, piece in enumerate(row):
                if piece is None:
                    continue

                for di, dj in self.DIRECTIONS:
                    ti = i
                    tj = j
                    for _ in range(self.NEXT_MOVE_RADIUS):
                        ti += di
                        tj += dj
                        if self.on_board(ti, tj) and self._state[ti][tj] is None:
                            the_move = ti, tj
                            if the_move not in generated_moves:
                                generated_moves.add(the_move)
                                yield the_move

    @classmethod
    def to_algebraic_notation(cls, i, j):
        return str(i + 1) + cls.COLUMN_HEADERS[j]

    @classmethod
    def load_homework_input(cls, file_path):
        board = cls()
        with open(file_path) as f:
            f_iter = iter(f)
            board.is_white_s_turn = next(f_iter).rstrip('\n') == 'WHITE'
            remaining_time = float(next(f_iter).rstrip('\n'))

            captures = tuple(map(int, next(f_iter).rstrip('\n').split(',')))
            board.pairs_captured[0] = captures[1]
            board.pairs_captured[1] = captures[0]

            for i, line in enumerate(f):
                for j, piece in enumerate(line.rstrip('\n')):
                    if piece != '.':
                        board._state[cls.BOARD_LENGTH - i - 1][j] = piece == 'w'
        return board, remaining_time


PLAYER_STATE_FILE_NAME = 'playdata.txt'
BACKED_UP_PLAYER_STATE_FILE_NAME = '{}_' + PLAYER_STATE_FILE_NAME

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('white', help='command line for the white player')
    parser.add_argument('black', help='command line for the black player')
    args = parser.parse_args()
    commands = args.black.split(' '), args.white.split(' ')

    # Remove state files from previous games.
    state_file_path = Path(PLAYER_STATE_FILE_NAME)
    state_file_path.unlink(missing_ok=True)
    for color in 'white', 'black':
        Path(BACKED_UP_PLAYER_STATE_FILE_NAME.format(color)).unlink(missing_ok=True)

    remaining_time = [100.0, 100.0]
    game = Pente()
    while game.result is None:
        player_index = int(game.is_white_s_turn)
        color = 'white' if game.is_white_s_turn else 'black'

        backed_up_state_file_path = Path(BACKED_UP_PLAYER_STATE_FILE_NAME.format(color))
        if backed_up_state_file_path.exists():
            backed_up_state_file_path.rename(state_file_path)

        with open('input.txt', 'w') as f:
            print(color.upper(), file=f)
            print(remaining_time[player_index], file=f)
            print(f'{game.pairs_captured[1]},{game.pairs_captured[0]}', file=f)
            f.write(str(game))

        subprocess.run(commands[player_index])

        if state_file_path.exists():
            state_file_path.rename(backed_up_state_file_path)
        move = open('output.txt').read().rstrip('\n')
        print(f'Turn {game.turn}, {color.capitalize()}:', move)
        game.move(move)
        game.print()
        print()

    print('White wins:', game.result)
