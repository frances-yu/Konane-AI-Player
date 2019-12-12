# main.py
# Main driver file

# ============= Imports ============= #
from Game import Game
from Human import Human

# ============ Constants ============ #
board_size = 4

# ============= Main ============= #
if __name__ == '__main__':
    human1 = Human('White')
    human2 = Human('Black')
    game = Game(human1, human2, board_size)
