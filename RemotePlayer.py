# RemotePlayer.py
# Contains all input streams and handling for remote player
from Game import Move
from Player import Player

class RemotePlayer(Player):
    def __init__(self, name, is_bottom_left, tn):
        super().__init__(name, is_bottom_left)
        self.tn = tn
        self.firstmove = True
        self.remotefirst = False

    def index_decoder(self, line):
        new_line = ""
        for x in line:
            if x != "[" and x != "]":
                new_line += x
        L = new_line.split(":")
        if len(L) == 2:
            tup = ((int(L[0]),int(L[1])),(int(L[0]),int(L[1])))
            return tup
        else:
            tup = ((int(L[0]),int(L[1])),(int(L[2]),int(L[3])))
            return tup

    def get_oppo_move(self, start_index):
        # start_index = 4 if "move", start_index = 8 if "removed"
        oppo_move = self.tn.read_until(b"\n").decode('ASCII')[:-1]
        print(oppo_move)
        print(oppo_move[start_index:])
        move_tuple = self.index_decoder(oppo_move[start_index:])
        print(move_tuple)
        return Move(move_tuple[0][0], move_tuple[0][1], move_tuple[1][0], move_tuple[1][1])

    def get_move(self, board, prev_move):
        # Input move with format ((r1,c1),(r2,c2)) where r1,c1,r2,c2 are 0-indexed positions starting from top left
        # For first two moves, move formatted as (r1,c1)
        # For example, ((1,2),(1,4)) will move a piece at row 1, col 2 to a space at row 1, col 4
        # ((0,0),(0,0)) will take from the top left space on the first move

        #try:
        # q = tn.read_until(b"\n").decode('ASCII')[:-1]
        # time_left = q[6:]
        # time_left = time_left[:-2]

        #if prev_move.r1 == -1 and prev_move.c1 == -1 and prev_move.r2 == -1 and prev_move.c2 == -1:
        if prev_move is None or (prev_move.r1 == -1 and prev_move.c1 == -1 and prev_move.r2 == -1 and prev_move.c2 == -1):
            #if remote player goes first
            #receive removed move from server and return get_move
            oppo_move = self.tn.read_until(b"\n").decode('ASCII')[:-1]
            print("hello")
            print(oppo_move)
            print(oppo_move[8:])
            move_tuple = self.index_decoder(oppo_move[8:])
            print(move_tuple)
            move: Move = Move(move_tuple[0][0], move_tuple[0][1], move_tuple[1][0], move_tuple[1][1])
            print("in prev move")
            self.remotefirst = True
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

            if self.firstmove:
                if self.remotefirst:
                    self.tn.read_until(b"?Remove:")
                    agent_move = b"[" + m1 + b":" + m2 + b"]"
                    self.tn.write(agent_move + b"\r\n")
                    print(agent_move.decode('ASCII'))

                    repeat_agent_move = self.tn.read_until(b"Removed:" + agent_move + b"\n").decode('ASCII')[:-1]
                    print(repeat_agent_move)

                    move = self.get_oppo_move(4)

                    self.firstmove = False

                else:
                    self.tn.read_until(b"?Remove:")
                    agent_move = b"[" + m1 + b":" + m2 + b"]"
                    self.tn.write(agent_move + b"\r\n")
                    print(agent_move.decode('ASCII'))

                    # state_color = self.tn.read_until(b"Color:" + b"\n").decode('ASCII')[:-1]
                    # print(state_color)

                    repeat_agent_move = self.tn.read_until(b"Removed:" + agent_move + b"\n").decode('ASCII')[:-1]
                    print(repeat_agent_move)

                    move = self.get_oppo_move(8)

                    self.firstmove = False

            else:
                agent_move = b"[" + m1 + b":" + m2 + b"]:[" + m3 + b":" + m4 + b"]"
                self.tn.write(agent_move + b"\r\n")
                print(agent_move.decode('ASCII'))

                repeat_agent_move = self.tn.read_until(b"Move" + agent_move + b"\n").decode('ASCII')[:-1]
                print(repeat_agent_move)

                move = self.get_oppo_move(4)

            # move_tuple = self.index_decoder(oppo_move[4:])
            # move: Move = Move(move_tuple[0][0], move_tuple[0][1], move_tuple[1][0], move_tuple[1][1])

        # except:
        #     move: Move = Move(-1, -1, -1, -1)

        print(move)
        return move
