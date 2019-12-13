# RemotePlayer.py
# Contains all input streams and handling for remote player
from Game import Move
from Player import Player

class RemotePlayer(Player):
    def __init__(self, name, is_bottom_left, tn):
        super().__init__(name, is_bottom_left)
        self.tn = tn

    def get_move(self, board, prev_move):
        # Input move with format ((r1,c1),(r2,c2)) where r1,c1,r2,c2 are 0-indexed positions starting from top left
        # For first two moves, move formatted as (r1,c1)
        # For example, ((1,2),(1,4)) will move a piece at row 1, col 2 to a space at row 1, col 4
        # ((0,0),(0,0)) will take from the top left space on the first move

        # ?Move(180000):
        # [2:0]:[0:0]
        # Move[2:0]:[0:0]
        # Move[2:1]:[0:1]
        # ?Move(162757):

        try:
            q = tn.read_until(b"\n").decode('ASCII')[:-1]
            time_left = q[6:]
            time_left = time_left[:-2]

            if prev_move is None:
                #if remote player goes first
                #receive move from server and return get_move
                oppo_move = tn.read_until(b"\n").decode('ASCII')[:-1]
                move_tuple = ((int(oppo_move[5]), int(oppo_move[7])),(int(oppo_move[11]), int(oppo_move[13])))
                move: Move = Move(move_tuple[0][0], move_tuple[0][1], move_tuple[1][0], move_tuple[1][1])
            else:
                #prev_move is in form ((?,?),(?,?))
                #if agent goes first
                #send move to server
                #wait
                #receive move from server and return get_move
                m1 = str(prev_move[0][0]).encode('ASCII')
                m2 = str(prev_move[0][1]).encode('ASCII')
                m3 = str(prev_move[1][0]).encode('ASCII')
                m4 = str(prev_move[1][1]).encode('ASCII')
                agent_move = b"[" + m1 + b":" + m2 + b"]:[" + m3 + b"]"
                tn.write(agent_move + b"\r\n")
                repeat = tn.read_until(b"\n").decode('ASCII')[:-1]

                oppo_move = tn.read_until(b"\n").decode('ASCII')[:-1]
                move_tuple = ((int(oppo_move[5]), int(oppo_move[7])),(int(oppo_move[11]), int(oppo_move[13])))
                move: Move = Move(move_tuple[0][0], move_tuple[0][1], move_tuple[1][0], move_tuple[1][1])

        except:
            move: Move = Move(-1, -1, -1, -1)
        return move
