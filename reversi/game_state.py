from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING
from concurrent.futures import ThreadPoolExecutor as ThreadPoolExecutor

if TYPE_CHECKING:
    from reversi import Reversi


class GameState:
    def __init__(self, game: Reversi, p: float = 1, r: float = 0) -> None:
        """
        Store a reversi object with a specific state in the game.board numpy array,
        probability of the children states (assuming equal probablity) and
        reward of reaching the current state
        Arguments:
            game -- a Reversi object

        Keyword Arguments:
            p -- equal probability for reaching the children states (default: {1})
            r -- reward of the current state (default: {0})
        """
        self.game = game
        self.children: dict[tuple[int, int], GameState] = {}
        self.p = p
        self.r = r

    def __str__(self):
        return f"p: {self.p}, r:{self.r}, next possible moves: {self.children.keys()}"

    def add(self, move: tuple[int, int], state: GameState):
        """A add a children state to the current state
        User will need to ensure the children state is a valid state

        Arguments:
            move -- a tuple of xy position a new piece is added
            state -- a GameState object of the resulting state after making the "move"
        """
        self.children[move] = state

    def V(self):
        """
        Calculate value for each state by estimating from reward of children states
        Returns:
            total value evaluated for the given state
        """
        if not self.children:
            return self.r
            
        # R(s) + V(s')
        total = self.r
        for m in self.children:
            child = self.children[m]
            total += child.V() * child.p
            
        return total


    def print_states(self, tab = 0):
        """method to pring the states and their children states

        Keyword Arguments:
            tab -- "tabify" at each generation (default: {0})
        """
        if len(self.children) == 0:
            return
        for move in self.children:
            print(f"{'    ' * tab}{tab}: {move}")
            self.children[move].print_states(tab + 1)


    @classmethod
    def build_model(cls, game, states, n_turns):
        """build a tree of "n_turns" number of turns starting from the current game state

        Arguments:
            game -- Reversi game object
            states -- GameState object for the current state
            n_turns -- number of turns to look ahead
            player -- 

        Returns:
            _description_
        """
        if n_turns == 0:
            return states
        valid_moves = game.get_valid_moves()
        if len(valid_moves) == 0:
            return states
        p = 1 / len(valid_moves)
    
        def process_move(m):
            r = len(game.find_flip(*m)) * game.player
            
            ## forcing a high reward at corners?
            ## does this work?
            x, y = m 
            if x in [0,7] and y in [0,7]:
                r += 1000 * game.player
                
            ## more reward if on edges?
            elif x in [0, 7] or y in [0, 7]:
                r += 100 * game.player
                
            game_prime = game.copy()
            game_prime.force_next_turn(*m)
            child = GameState(game_prime, p, r)
            return m, child

        with ThreadPoolExecutor() as executor:
            results = executor.map(process_move, valid_moves)

        for move, child in results:
            states.add(move, child)
            cls.build_model(child.game, child, n_turns - 1)

        return states


    ## implemented above using Threading
    # @classmethod
    # def build_model(cls, game, states, n_turns, player) -> GameState:
    #     """build a tree of "n_turns" number of turns starting from the current game state

    #     Arguments:
    #         game -- _description_
    #         states -- _description_
    #         n_turns -- _description_
    #         player -- _description_

    #     Returns:
    #         _description_
    #     """
    #     if n_turns == 0:
    #         return states
    #     valid_moves = game.get_valid_moves()
    #     if len(valid_moves) == 0:
    #         return states
    #     p = 1 / len(valid_moves)
    #     for m in valid_moves:
    #         r = len(game.find_flip(*m)) * (1 if game.player == player else -1)
    #         game_prime = game.copy()
    #         game_prime.force_next_turn(*m)
    #         child = GameState(game_prime, p, r)
    #         states.add(m, child)
    #         cls.build_model(game_prime, child, n_turns - 1, player)
    #     return states
    

if __name__ == '__main__':
    ...
