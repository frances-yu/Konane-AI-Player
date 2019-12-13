# main.py
# Main driver file

# ============= Imports ============= #
from Game import Game
from Human import Human
from Agent import Agent
from RemotePlayer import RemotePlayer

import sys
import telnetlib

# ============ Constants ============ #
board_size = 18
tn_ip = "artemis.engr.uconn.edu"
tn_port = "4705"
tn_username = b"3333"
tn_password = b"3333"
tn_opponent = b"4444"
waitfor = b"Game:"

# ============ Functions ============ #
def telnet():
    try:
        tn = telnetlib.Telnet(tn_ip, tn_port, 15)
    except:
        print("Unable to connect to Telnet server: " + tn_ip)
        return
    tn.set_debuglevel(100)
    tn.read_until(b"?Username:")
    tn.write(tn_username + b"\r\n")
    tn.read_until(b"?Password:")
    tn.write(tn_password + b"\r\n")
    tn.read_until(b"?Opponent:")
    tn.write(tn_opponent + b"\r\n")
    tn.read_until(waitfor)
    print("Game authenticated")

    games = tn.read_until(b"\n").decode('ASCII')[:-1]
    #print(games)
    r1 = tn.read_until(b"\n").decode('ASCII')[:-1]
    print(r1)
    #Color:????? or Player:1

    if r1 == "Player:1":
        goes_first = True
        color = "WHITE"
        # first_move = "NONE"
    else:
        goes_first = False
        color = r1[6:]
        #print(color)
        #WHITE or BLACK
        r2 = tn.read_until(b"\n").decode('ASCII')[:-1]
        print(r2)
        #Player 2
        # r3 = tn.read_until(b"\n").decode('ASCII')[:-1]
        # print(r3)
        #Removed:[?:?]
        # first_move = r3[8:]
        # print(first_move)
        #[?:?]

    return tn, color, goes_first

# ============= Main ============= #
if __name__ == '__main__':
    tn, c, gf = telnet()

    if gf:
        agent1 = Agent("WHITE", False)
        remoteplayer2 = RemotePlayer("BLACK", True, tn)
        game = Game(agent1, remoteplayer2, board_size)
    else:
        if c == "WHITE":
            remoteplayer1 = RemotePlayer("BLACK", True, tn)
            agent2 = Agent(c, False)
            game = Game(remoteplayer1, agent2, board_size)
        else:
            remoteplayer1 = RemotePlayer("WHITE", False, tn)
            agent2 = Agent(c, True)
            game = Game(remoteplayer1, agent2, board_size)

    # if c == "NONE" and gf == True:
    #     agent1 = Agent("WHITE", gf)
    #     #agentc = agent1.get_color()
    #     #if agentc == "WHITE":
    #     if c == "NONE":
    #         remoteplayer2 = RemotePlayer("BLACK", False)
    #     else:
    #         remoteplayer2 = RemotePlayer("WHITE", False)
    # else:
    #     remoteplayer1 = RemotePlayer(c, gf)
    #     if c == "WHITE":
    #         agent2 = Agent("BLACK", False)
    #     else:
    #         agent2 = Agent("WHITE", False)

    # human1 = Human('White', True)
    # human2 = Human('Black', False)
    # game = Game(human1, human2, board_size)
