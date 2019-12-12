# RemotePlayer.py

from Game import Move
from Player import Player


class RemotePlayer(Player):
    def __init__(self, name, is_top_left):
        super().__init__(name, is_top_left)
        # TODO setup more object variables

    def get_move(self, board):
        # wait for move from server and output to move
        move: Move = None
        # TODO the hard shit
        return move
