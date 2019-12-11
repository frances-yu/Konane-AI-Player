# Human.py
# Contains all input streams and handling for human player

from Player import Player


class Human(Player):
    def __init__(self, name):
        super().__init__(name)

    def get_move(self):
        # Input move with format ((r1,c1),(r2,c2)) where r1,c1,r2,c2 are 0-indexed positions starting from top left
        # For example, ((1,2),(1,4)) will move a piece at row 1, col 2 to a space at row 1, col 4
        move = eval(input("Enter move for " + self.name + ": "))
        return