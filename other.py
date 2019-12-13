# main.py
# Main driver file

# ============= Imports ============= #
from Game import Game
from Human import Human
from Agent import Agent

# ============= Main ============= #
if __name__ == '__main__':
    agent1 = Agent('WHITE', False)
    agent2 = Agent('BLACK', True)
    human1 = Human('WHITE', False)
    human2 = Human('BLACK', True)
    game = Game(agent2, agent1, 8)
