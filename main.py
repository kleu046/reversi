import numpy as np
from typing import Any
from reversi.reversi import Reversi


def main():
    game = Reversi()
    
    # game.board = np.array([
    #     [-1, -1, -1, -1, -1, -1, -1, -1],
    #     [-1,  1,  1,  1,  1,  1,  1, -1],
    #     [-1,  1,  1,  1,  1,  1,  1, -1],
    #     [-1,  1,  1,  1,  1,  1,  1, -1],
    #     [-1,  1,  1,  1,  1,  1,  1, -1],
    #     [-1,  1,  1,  1,  1,  1,  1, -1],
    #     [-1,  1,  1,  1,  1,  1,  1, -1],
    #     [ 0,  0,  0,  0,  0,  0,  0,  0]])

    consecutive_no_move = 0
    while consecutive_no_move < 2:
        print(game)
        if game.turn() == -999:
            consecutive_no_move += 1
        else:
            consecutive_no_move = 0
        if not (game.board == 0).any():
            break    
    print(game)
    
    count_x = (game.board == -1).sum()
    count_o = (game.board == 1).sum()
    print(f'{"X" if count_x > count_o else "O"} wins with {max(count_x, count_o)} pieces\n')
    
if __name__ == "__main__":
    main()
