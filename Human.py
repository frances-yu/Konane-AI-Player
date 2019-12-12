# Human.py
# Contains all input streams and handling for human player
from Game import Move
from Player import Player


class Human(Player):
    def __init__(self, name, is_top_left):
        super().__init__(name, is_top_left)

    def get_move(self, board):
        # Input move with format ((r1,c1),(r2,c2)) where r1,c1,r2,c2 are 0-indexed positions starting from top left
        # For first two moves, move formatted as (r1,c1)
        # For example, ((1,2),(1,4)) will move a piece at row 1, col 2 to a space at row 1, col 4

        try:
            move_tuple = eval(input("Enter move for " + self.name + ": "))
            move: Move = Move(move_tuple[0][0], move_tuple[0][1], move_tuple[1][0], move_tuple[1][1])
        except:
            move: Move = Move(-1, -1, -1, -1)
        return move
