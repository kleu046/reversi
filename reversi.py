import numpy as np
from .game_state import GameState

class Reversi:
    def __init__(self, size: int = 8) -> None:
        self.size = size
        self.board = np.zeros((size, size), dtype = np.int8)
        self.board[size // 2 - 1, size // 2 - 1] = self.board[size // 2, size // 2] = 1
        self.board[size // 2, size // 2 - 1] = self.board[size // 2 - 1, size // 2] = -1
        self.player = -1 # traditionally black go first
        
    def copy(self):
        new_game = Reversi()
        new_game.size = self.size
        new_game.board = self.board.copy()
        new_game.player = self.player
        return new_game
    
    def force_next_turn(self, x: int | None = None, y: int | None = None, player: int | None = None):
        if not player: # unless specified, player is the current player
            player = self.player
        if x is not None and y is not None: # if x and y are specified, place the piece
            to_flip = self.find_flip(x, y) 
            if to_flip:
                self[x, y] = player
                self.flip(to_flip)
        self.player = -self.player
        return

    def __getitem__(self, key):
        return self.board[key]
    
    def __str__(self):
        return self.pretty_board()       
    
    def __setitem__(self, key, value):
        self.board[key] = value
        
    def pretty_board(self) -> str:
        s = ' ====' + '======='.join([str(i) for i in range(self.size)]) + '====\n'

        for r, row in enumerate(self.board):
            for i, c in enumerate(row):
                if i == 0:
                    s += str(r)
                s += '|   ' + (('O' if c == 1 else 'X') if c != 0 else ' ') + '   '
            s += '|\n'
            if 0 <= r < self.size - 1:
                s += ' ----' + '-------'.join(["-" for i in range(self.size)]) + '----\n'
        s += ' ====' + '======='.join(["=" for i in range(self.size)]) + '====\n'
        return s

    def find_best_ai_move(self, valid_moves):
        best_move = []
        best_V = -999

        for move in valid_moves:
            self_prime = self.copy()
            self_prime.force_next_turn(*move)
            mod = GameState.build_model(self_prime, GameState(self_prime.board), 4, self.player)
            V = mod.V()
            if V > best_V:
                best_move = [move]
                best_V = V
            elif V == best_V:
                best_move.append(move)
                best_V = V
        return best_move
    
    def prompt_player_move(self, valid_moves) -> tuple[int, int]:
        while True:
            try:
                x = int(input(f"Player {'X' if self.player == -1 else 'O'}, enter row: "))
                y = int(input(f"Player {'X' if self.player == -1 else 'O'}, enter column: "))
                if (x, y) in valid_moves:
                    break
            except ValueError:
                continue
        return x, y

    def turn(self) -> int | None:
        valid_moves = self.get_valid_moves()
        if len(valid_moves) == 0:
            self.player = -self.player
            return -999
        else:
            if self.player == 1:
                best_move = self.find_best_ai_move(valid_moves)
                print(f"Player O row: {best_move[0][0]}, {best_move[0][1]}")
                self.force_next_turn(*best_move[0])
                return 0
            else:
                x, y = self.prompt_player_move(valid_moves)
                self.flip(valid_moves[(x, y)])
                self[x, y] = self.player
                self.player = -self.player
                return 0


    def is_valid_move(self, x: int, y: int) -> list[tuple[int, int]] | None:
        """
        1.	Opposing Disc Line: The disc must be placed adjacent to at least one opponent’s disc.
        2.	Sandwich Formation: The placed disc must create a line (horizontal, vertical, or diagonal) where one or more opponent’s discs are “sandwiched” between the new disc and another of the player’s discs already on the board.
        3.	At Least One Capture: The move must result in at least one opponent’s disc being flipped. If no such move is possible, the player must pass their turn.
        """
        if not self.is_within_board(x, y) or not self.is_empty(x, y):  # valid x and valid y must be the first checks or self[x, y] could return error
            return

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.is_within_board(nx, ny) and self[nx, ny] == -self.player:
                    # print(f"({x}, {y}) is within the board and is next to an opponent piece")
                    # -player == opponent # check if the neighbouring position is a opponent
                    to_flip = self.find_flip(x, y) # has a valid flip
                    if len(to_flip) > 0:
                        return to_flip

        return

    def is_within_board(self, x, y) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size


    def is_empty(self, x, y) -> bool:
        return self[x, y] == 0


    def find_flip(self, x, y) -> list[tuple[int, int]]:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        to_flip_all_direction = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            to_flip_current_direction = []
            
            if not self.is_within_board(nx, ny) or self[nx, ny] != -self.player:
                continue
            
            while self.is_within_board(nx, ny) and self[nx, ny] == -self.player: # -self.player == opponent
                to_flip_current_direction.append((nx, ny))
                nx += dx
                ny += dy
            # after the last opponent piece, it should be a player piece
            if 0 <= nx < self.size and 0 <= ny < self.size and self[nx, ny] == self.player:
                to_flip_all_direction.extend(to_flip_current_direction)
        return to_flip_all_direction


    def flip(self, to_flip) -> None:
        """
        Flip the pieces in the to_flip list

        Arguments:
            to_flip -- list of coordinates to flip into the current player
        """
        for x, y in to_flip:
            self[x, y] = self.player


    def get_valid_moves(self) -> dict[tuple[int, int], list[tuple[int, int]]]:
        """
        Check if there are any valid moves for the current player
        Keep track of checked positions
        Only check positions where self[x, y] == 0 - the only possible moves
        
        Returns:
            valid_moves as dict of valid move xy coordiates and positions that can be flipped
        """
        valid_moves = {}
        pieces = np.where(self.board != 0)
        checked = set()
        
        for x, y in zip(pieces[0], pieces[1]):
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in checked and self.is_within_board(nx, ny) and self[nx, ny] == 0:
                        to_flip = self.find_flip(nx, ny)
                        if len(to_flip) > 0:
                            valid_moves[(nx, ny)] = to_flip
                        checked.add((nx, ny))
        return valid_moves




# class State:
#     def __init__(self, game: Reversi, p: float = 1, r: float = 0) -> None:
#         self.game = game
#         self.children = {}
#         self.p = p
#         self.r = r

#     def __str__(self):
#         return f"p: {self.p}, r:{self.r}, next possible moves: {self.children.keys()}"

#     def add(self, move, state):
#         self.children[move] = state

#     def V(self):
#         if not self.children:
#             return self.r
            
#         # R(s) + V(s') + V(s")
#         total = self.r
#         for m in self.children:
#             child = self.children[m]
#             child_value = child.V() * child.p
#             total += child_value
            
#             for n in child.children:
#                 grandchild = child.children[n]
#                 total += grandchild.V() * grandchild.p * child.p
                
#         return total


#     def print_states(self, tab = 0):
#         if len(self.children) == 0:
#             return
#         for move in self.children:
#             print(f"{'    ' * tab} {move}")
#             self.children[move].print_states(tab + 1)


#     @classmethod
#     def build_model(cls, game, states, n_turns, player):
#         if n_turns == 0:
#             return states
#         valid_moves = game.get_valid_moves()
#         if len(valid_moves) == 0:
#             return states
#         p = 1 / len(valid_moves)
#         for m in valid_moves:
#             r = len(game.find_flip(*m)) * (1 if game.player == player else -1)
#             game_prime = game.copy()
#             game_prime.force_next_turn(*m)
#             child = State(game_prime, p, r)
#             states.add(m, child)
#             cls.build_model(game_prime, child, n_turns - 1, player)
#         return states
