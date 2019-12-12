# main.py
# Main driver file

# ============= Imports ============= #
from Game import Game
from Human import Human
from Agent import Agent

import sys
import telnetlib

# ============ Constants ============ #
board_size = 18
tn_ip = "artemis.engr.uconn.edu"
tn_port = "4705"
tn_username = b"4402"
tn_password = b"4401"
tn_opponent = b"2044"
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
    r = tn.read_some()


# ============= Main ============= #
if __name__ == '__main__':
    color, goes_first = telnet()

    agent1 = Agent('White', True)
    agent2 = Agent('Black', False)
    game = Game(agent1, agent2, board_size)
