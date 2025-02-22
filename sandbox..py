from reversi import Reversi
import numpy as np

def main():
    game = Reversi(level=4)
    compute_P(game)

def compute_P(game):
    is_empty = game.board == 0
    is_opponent = game.board == -game.player
    padded_board = np.pad(is_opponent, pad_width=1, mode='constant')
    print(padded_board)
    
    # neighbors = np.zeros_like(game.board, dtype=bool)
    
    # for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
    #     neighbors |= padded_board[1+dx:game.size+1+dx, 1+dy:game.size+1+dy]
    
    # print(is_empty & neighbors)
    
if __name__ == "__main__":
    main()


