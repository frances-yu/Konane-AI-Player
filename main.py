# main.py
# Main driver file

# ============= Imports ============= #
from Game import Game
from Human import Human

# ============ Constants ============ #
board_size = 4

# ============= Main ============= #
if __name__ == '__main__':
    human1 = Human('P1')
    human2 = Human('P2')
    game = Game(human1, human2, board_size)
