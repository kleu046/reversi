from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from reversi import Reversi

class GameState:
    def __init__(self, game: Reversi, p: float = 1, r: float = 0) -> None:
        self.game = game
        self.children: dict[tuple[int, int], GameState] = {}
        self.p = p
        self.r = r

    def __str__(self):
        return f"p: {self.p}, r:{self.r}, next possible moves: {self.children.keys()}"

    def add(self, move, state):
        self.children[move] = state

    def V(self):
        if not self.children:
            return self.r
            
        # R(s) + V(s') + V(s")
        total = self.r
        for m in self.children:
            child = self.children[m]
            child_value = child.V() * child.p
            total += child_value
            
            for n in child.children:
                grandchild = child.children[n]
                total += grandchild.V() * grandchild.p * child.p
                
        return total


    def print_states(self, tab = 0):
        if len(self.children) == 0:
            return
        for move in self.children:
            print(f"{'    ' * tab} {move}")
            self.children[move].print_states(tab + 1)


    @classmethod
    def build_model(cls, game, states, n_turns, player):
        if n_turns == 0:
            return states
        valid_moves = game.get_valid_moves()
        if len(valid_moves) == 0:
            return states
        p = 1 / len(valid_moves)
        for m in valid_moves:
            r = len(game.find_flip(*m)) * (1 if game.player == player else -1)
            game_prime = game.copy()
            game_prime.force_next_turn(*m)
            child = GameState(game_prime, p, r)
            states.add(m, child)
            cls.build_model(game_prime, child, n_turns - 1, player)
        return states


if __name__ == '__main__':
    ...