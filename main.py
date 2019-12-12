# main.py
# Main driver file

# ============= Imports ============= #
from Game import Game
from Human import Human
from Agent import Agent

# ============ Constants ============ #
board_size = 8

# ============= Main ============= #
if __name__ == '__main__':

    human1 = Human('White', True)
    human2 = Human('Black', False)
    game = Game(human1, human2, board_size)
