from typing import Optional
from argparse import ArgumentParser
from pathlib import Path
import subprocess


class Pente:
    State = tuple[list[Optional[bool]], ...]

    BOARD_LENGTH = 19
    COLUMN_HEADERS = 'ABCDEFGHJKLMNOPQRST'
    DIRECTIONS = (1, 0), (0, 1), (1, 1), (-1, 1)
    N_PIECES_WIN = N_CAPTURES_WIN = 5

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
            if (self._state[first_i][first_j] is not self._state[i][j]
                    and self._state[second_i][second_j] is not self._state[i][j]):
                self._state[first_i][first_j] = None
                self._state[second_i][second_j] = None
                return True
        return False

    def move(self, pos: str):
        i = int(pos[:-1]) - 1
        j = self.COLUMN_HEADERS.index(pos[-1])
        self._state[i][j] = self.is_white_s_turn

        player_index = int(self.is_white_s_turn)
        for di, dj in self.DIRECTIONS:
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
        print('  ', ' '.join(self.COLUMN_HEADERS))
        for i, row in enumerate(reversed(self._state)):
            print(format(self.BOARD_LENGTH - i, '2d'), end=' ')
            print(' '.join(
                '.' if piece is None else 'w' if piece else 'b' for piece in row
            ))

    @classmethod
    def to_algebraic_notation(cls, i, j):
        return str(i + 1) + cls.COLUMN_HEADERS[j]


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

        print(f'Turn {game.turn},', color.capitalize())
        with open('input.txt', 'w') as f:
            print(color.upper(), file=f)
            print(remaining_time[player_index], file=f)
            print(f'{game.pairs_captured[1]},{game.pairs_captured[0]}', file=f)
            f.write(str(game))

        subprocess.run(commands[player_index])

        if state_file_path.exists():
            state_file_path.rename(backed_up_state_file_path)
        move = open('output.txt').read().rstrip('\n')
        game.move(move)
        game.print()
        print()

    print('White wins:', game.result)
