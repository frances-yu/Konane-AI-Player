# RemotePlayer.py
# Contains all input streams and handling for remote player
from Game import Move
from Player import Player

class RemotePlayer(Player):
    def __init__(self, name, is_bottom_left, tn):
        super().__init__(name, is_bottom_left)
        self.tn = tn
        self.remotefirst = True

    def index_decoder(self, line):
        new_line = ""
        for x in line:
            if x != "[" or x != "]":
                new_line += x
        L = new_line.split(":")
        if len(L) == 2:
            tup = ((L[0],L[1]),(L[0],L[1]))
            return tup
        else:
            tup = ((L[0],L[1]),(L[3],L[4]))
            return tup

    def get_move(self, board, prev_move):
        # Input move with format ((r1,c1),(r2,c2)) where r1,c1,r2,c2 are 0-indexed positions starting from top left
        # For first two moves, move formatted as (r1,c1)
        # For example, ((1,2),(1,4)) will move a piece at row 1, col 2 to a space at row 1, col 4
        # ((0,0),(0,0)) will take from the top left space on the first move

        try:
            # q = tn.read_until(b"\n").decode('ASCII')[:-1]
            # time_left = q[6:]
            # time_left = time_left[:-2]

            if prev_move.r1 == -1 and prev_move.c1 == -1 and prev_move.r2 == -1 and prev_move.c2 == -1:
                #if remote player goes first
                #receive removed move from server and return get_move
                oppo_move = self.tn.read_until(b"\n").decode('ASCII')[:-1]
                print(oppo_move)
                print(oppo_move[8:])
                ###move_tuple = ((int(oppo_move[10]), int(oppo_move[12])),(int(oppo_move[10]), int(oppo_move[12])))
                move_tuple = self.index_decoder(oppo_move[8:])
                print(move_tuple)
                move: Move = Move(move_tuple[0][0], move_tuple[0][1], move_tuple[1][0], move_tuple[1][1])
                self.remotefirst = True
                print("in prev move")
            else:
                #prev_move is in form ((?,?),(?,?))
                #if agent goes first
                #send move to server
                #wait
                #receive move from server and return get_move
                m1 = str(prev_move.r1).encode('ASCII')
                m2 = str(prev_move.c1).encode('ASCII')
                m3 = str(prev_move.r2).encode('ASCII')
                m4 = str(prev_move.c2).encode('ASCII')

                if self.remotefirst:
                    self.remotefirst = False
                    agent_move = b"[" + m1 + b":" + m2 + b"]"
                    print(agent_move.decode('ASCII'))
                    self.tn.write(agent_move + b"\r\n")

                    repeat = self.tn.read_until(b"\n").decode('ASCII')[:-1]
                    print(repeat)

                    oppo_move = self.tn.read_until(b"\n").decode('ASCII')[:-1]
                    print(oppo_move)

                else:
                    agent_move = b"[" + m1 + b":" + m2 + b"]:[" + m3 + b":" + m4 + b"]"

                    print(agent_move.decode('ASCII'))
                    self.tn.write(agent_move + b"\r\n")

                    repeat = self.tn.read_until(b"\n").decode('ASCII')[:-1]
                    print(repeat)

                    oppo_move = self.tn.read_until(b"\n").decode('ASCII')[:-1]
                    print(oppo_move)

                move_tuple = self.index_decoder(oppo_move[4:])
                move: Move = Move(move_tuple[0][0], move_tuple[0][1], move_tuple[1][0], move_tuple[1][1])

        except:
            move: Move = Move(-1, -1, -1, -1)

        print(move)
        return move
