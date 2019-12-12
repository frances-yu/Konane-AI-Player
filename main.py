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

    agent1 = Agent('White', True)
    agent2 = Agent('Black', False)
    game = Game(agent1, agent2, board_size)
