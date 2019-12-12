# main.py
# Main driver file

# ============= Imports ============= #
from Game import Game
from Human import Human
from Agent import Agent

import sys
import telnetlib

# ============ Constants ============ #
board_size = 8
tn_ip = "artemis.engr.uconn.edu"
tn_port = "4705"
tn_username = b"4402"
tn_password = b"4401"
tn_opponent = b"2044"
waitfor = b"Game:3812"

# ============ Functions ============ #
def telnet():
    try:
        tn = telnetlib.Telnet(tn_ip, tn_port, 15)
    except:
        print("Unable to connect to Telnet server: " + tn_ip)
        return
    tn.set_debuglevel(100)
    tn.read_until(b"?Username:")
    tn.write(tn_username + "\r\n")
    tn.read_until(b"?Password:")
    tn.write(tn_password + "\r\n")
    tn.read_until(b"?Opponent:")
    tn.write(tn_opponent + "\r\n")
    tn.read_until(waitfor)
    print("Game authenticated")

# ============= Main ============= #
if __name__ == '__main__':
    telnet()

    human1 = Human('White', True)
    human2 = Human('Black', False)
    game = Game(human1, human2, board_size)
