from reversi import Reversi
import numpy as np
import time


def main():
    game = Reversi(level=3)

    game.board = np.array([
            [ 0, 0, 0, 0, 0, -1, 0, 0],
            [ 0, 0, 0, -1, 0, 1, 1, 1],
            [ 0, 0, 1, -1, 1, 1, 0, 0],
            [ 0, 0, 0, -1, 1, 1, 0, 0],
            [ 0, 0, 0, -1, 1, 1, 0, 0],
            [ 0, 0, -1, -1, -1, -1, -1, 0],
            [ 0, 0, 1, 1, 1, 1, 1, 0],
            [ 0, 0, 0, -1, 0, 1, 1, 1],])


def time_function(func, *args, repeat=10, **kwargs):
    total_time = 0
    for _ in range(repeat):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / repeat
    print(f"Average time taken: {average_time:.6f} seconds")


def get_valid_moves(game):       
    is_empty = (game.board == 0)
    is_opponent = (game.board == -game.player)
    padded_board = np.pad(is_opponent, pad_width=1, mode='constant')

    # neighbor check
    neighbors = np.zeros_like(game.board, dtype=bool)
    
    for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        neighbors |= padded_board[1+dx:game.size+1+dx, 1+dy:game.size+1+dy]
    
    potential_moves = is_empty & neighbors
    valid_moves = np.zeros((game.size, game.size))
    to_flip = {}
    
    # is a empty position next to a opponent piece?
    for i in range(game.size):
        for j in range(game.size):
            if is_empty[i, j] == 1 and potential_moves[i, j]:
                # does a flip exist
                to_flip_in_all_directions = game.find_flip(i, j)
                if len(to_flip_in_all_directions) > 0:
                    valid_moves[i, j] = 1
                    to_flip[(i, j)] = to_flip_in_all_directions

    return to_flip

