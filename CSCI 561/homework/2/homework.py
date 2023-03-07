from pathlib import Path
import pickle
from copy import deepcopy

from engine import Pente, PLAYER_STATE_FILE_NAME

DEFAULT_MAX_DEPTH = 3


def minimax(
    game: Pente, alpha: int = - Pente.MAX_UTILITY, beta: int = Pente.MAX_UTILITY,
    max_depth=DEFAULT_MAX_DEPTH
) -> tuple[int, tuple[int, int]]:
    best_move = (0, 0)
    if game.is_white_s_turn:
        best_utility = - Pente.MAX_UTILITY
        for move in game.next_moves():
            new_game = deepcopy(game)
            new_game.move(move)
            utility = minimax_recursive(new_game, 2, max_depth, alpha, beta)
            if best_utility < utility:
                best_utility = utility
                best_move = move

            if alpha < best_utility:
                alpha = best_utility
            if alpha >= beta:
                break
    else:
        best_utility = Pente.MAX_UTILITY
        for move in game.next_moves():
            new_game = deepcopy(game)
            new_game.move(move)
            utility = minimax_recursive(new_game, 2, max_depth, alpha, beta)
            if best_utility > utility:
                best_utility = utility
                best_move = move

            if beta > best_utility:
                beta = best_utility
            if alpha >= beta:
                break

    return best_utility, best_move


def minimax_recursive(game: Pente, depth: int, max_depth: int, alpha: int, beta: int) -> int:
    if depth > max_depth:
        return game.evaluate()
    if game.result is not None:
        return game.MAX_UTILITY if game.result else - game.MAX_UTILITY

    depth += 1
    if game.is_white_s_turn:
        best_utility = - Pente.MAX_UTILITY
        for move in game.next_moves():
            new_game = deepcopy(game)
            new_game.move(move)
            utility = minimax_recursive(new_game, depth, max_depth, alpha, beta)
            if best_utility < utility:
                best_utility = utility

            if alpha < best_utility:
                alpha = best_utility
            if alpha >= beta:
                break
    else:
        best_utility = Pente.MAX_UTILITY
        for move in game.next_moves():
            new_game = deepcopy(game)
            new_game.move(move)
            utility = minimax_recursive(new_game, depth, max_depth, alpha, beta)
            if best_utility > utility:
                best_utility = utility

            if beta > best_utility:
                beta = best_utility
            if alpha >= beta:
                break

    return best_utility


if __name__ == '__main__':
    game, remaining_time = Pente.load_homework_input('input.txt')
    state_file_path = Path(PLAYER_STATE_FILE_NAME)
    if state_file_path.exists():
        with open(state_file_path, 'rb') as f:
            state = pickle.load(f)
            game.turn = state['turn']
    else:
        state = {'turn': 0}

    move = '10K'
    # preconfigured moves
    if game.turn == 0:
        if not game.is_white_s_turn:
            move = '9K'
    elif game.turn == 1 and game.is_white_s_turn:
        if game.turn == 1:
            # Find the black's first move.
            for i, row in enumerate(game._state):
                for j, piece in enumerate(row):
                    if piece is False:
                        break
                else:
                    continue
                break

            di = i - Pente.CENTER_POS
            dj = j - Pente.CENTER_POS
            # White's second move is on the horizontal or vertical axis and
            # 3 intersections away from its first move.
            if abs(di) < abs(dj):
                move = Pente.to_algebraic_notation(6 if di < 0 else 12, Pente.CENTER_POS)
            else:
                move = Pente.to_algebraic_notation(Pente.CENTER_POS, 6 if dj < 0 else 12)
    else:
        move = Pente.to_algebraic_notation(*minimax(game)[1])

    state['turn'] += 1
    with open(state_file_path, 'wb') as f:
        pickle.dump(state, f)

    with open('output.txt', 'w') as f:
        print(move, file=f)
