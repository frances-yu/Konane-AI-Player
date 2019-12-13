# RemotePlayer.py

from Game import Move
from Player import Player


class RemotePlayer(Player):
<<<<<<< HEAD
    def __init__(self, name, is_bottom_left):
        super().__init__(name, is_bottom_left)
        # TODO setup more object variables
=======
    def __init__(self, color, goes_first):
        super().__init__(color, goes_first)

    def get_color(self):
        return self.color

    def get_move(self, board):
        # wait for move from server and output to move
        try:
            #Move[2:1]:[0:1]
            move_tuple = tn.read_until(b"\n").decode('ASCII')[:-1]
            move: Move = Move(move_tuple[0][0], move_tuple[0][1], move_tuple[1][0], move_tuple[1][1])
        except:
            move: Move = Move(-1, -1, -1, -1)
        return move



    def __init__(self, name, is_top_left):
        super().__init__(name, is_top_left)
>>>>>>> 3739de83083520525054fc8105424ccb4af50d1c

    def get_move(self, board):
        # Input move with format ((r1,c1),(r2,c2)) where r1,c1,r2,c2 are 0-indexed positions starting from top left
        # For first two moves, move formatted as (r1,c1)
        # For example, ((1,2),(1,4)) will move a piece at row 1, col 2 to a space at row 1, col 4
        # ((0,0),(0,0)) will take from the top left space on the first move
        try:
            move_tuple = eval(input("Enter move for " + self.name + ": "))
            move: Move = Move(move_tuple[0][0], move_tuple[0][1], move_tuple[1][0], move_tuple[1][1])
        except:
            move: Move = Move(-1, -1, -1, -1)
        return move
