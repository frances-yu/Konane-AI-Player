# main.py
# Main driver file

# ============= Imports ============= #
from Game import Game
from Human import Human
from Agent import Agent

# ============= Main ============= #
if __name__ == '__main__':
    agent1 = Agent('White', True)
    agent2 = Agent('Black', False)
    human1 = Human('White', True)
    human2 = Human('Black', False)
    game = Game(agent1, agent2, 18)
