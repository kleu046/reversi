from reversi import Reversi
import numpy as np

game = Reversi()

def test_is_within_board():
    assert game.is_within_board(0, 0) == True
    assert game.is_within_board(7, 7) == True
    assert game.is_within_board(0, 7) == True
    assert game.is_within_board(7, 0) == True
    assert game.is_within_board(-1, 0) == False
    assert game.is_within_board(0, -1) == False
    assert game.is_within_board(8, 0) == False
    assert game.is_within_board(0, 8) == False
    assert game.is_within_board(-1, -1) == False
    assert game.is_within_board(8, 8) == False
    
def test_is_empty():
    assert game.is_empty(3, 3) == False
    assert game.is_empty(2, 3) == True
    assert game.is_empty(3, 2) == True
    
def test_get_valid_moves():
    assert list(game.get_valid_moves().keys()) == [(2, 3), (3, 2), (4, 5), (5, 4)]

def test_is_valid_move():
    assert game.is_valid_move(2, 3) == [(3, 3)]
    assert game.is_valid_move(3, 2) == [(3, 3)]
    assert game.is_valid_move(7, 7) is None
    assert game.is_valid_move(0, 0) is None
    
def test_has_flip():
    assert game.find_flip(2, 3) == [(3, 3)]
    assert game.find_flip(3, 2) == [(3, 3)]
    assert game.find_flip(7, 7) == []
    assert game.find_flip(0, 0) == []
    
    game.board = np.array([
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, -1, 0, 1, 1, 1],
        [ 0, 0, 1, -1, 1, 1, 0, 0],
        [ 0, 0, 0, -1, 1, 1, 0, 0],
        [ 0, 0, 0, -1, 1, 1, 0, 0],
        [ 0, 0, -1, -1, -1, -1, -1, 0],
        [ 0, 0, 1, 1, 1, 1, 1, 0],
        [ 0, 0, 0, -1, 0, 1, 1, 1],])
    
    assert game.find_flip(0, 5) == [(1, 5), (2, 5), (3, 5), (4, 5)]
    
    game.board = np.array([
        [ 0, 0, 0, 0, 0, -1, 0, 0],
        [ 0, 0, 0, -1, 0, 1, 1, 1],
        [ 0, 0, 1, -1, 1, 1, 0, 0],
        [ 0, 0, 0, -1, 1, 1, 0, 0],
        [ 0, 0, 0, -1, 1, 1, 0, 0],
        [ 0, 0, -1, -1, -1, -1, -1, 0],
        [ 0, 0, 1, 1, 1, 1, 1, 0],
        [ 0, 0, 0, -1, 0, 1, 1, 1],]) * -1
    
    assert game.find_flip(3, 2) == [(3,3),(4,3),(5,4)]
    
def test_copy():
    game_copy = game.copy()
    assert np.array_equal(game_copy.board, game.board)
    assert game.player == game_copy.player
    assert game.size == game_copy.size
    
def test_force_next_turn():
    game_copy = game.copy()
    game_copy.force_next_turn(3,2)
    game.force_next_turn(3, 2)
    assert game_copy.player == game.player
    assert np.array_equal(game_copy.board, game.board)
    
def test_flip():
    game_copy = game.copy()
    game_copy.flip([(3, 2)])
    assert game_copy[3,2] == game_copy.player