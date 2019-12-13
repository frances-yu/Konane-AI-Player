# main.py
# Main driver file

# ============= Imports ============= #
from Game import Game
from Human import Human
from Agent import Agent

# ============= Main ============= #
if __name__ == '__main__':
    agent1 = Agent('White', False)
    agent2 = Agent('Black', True)
    human1 = Human('White', False)
    human2 = Human('Black', True)
    game = Game(agent1, agent2, 18)
