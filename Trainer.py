from Game import Game
from Agent import Agent
from random import randint
from random import seed 


def random_weights(seed):
    w = []

    for _ in range(4):
        w.append(randint(0, 20))
    return w


def train(size = 10, epochs = 5):

    win = []
    lose = []

    a1 = Agent("White", False)
    a2 = Agent("Black", True)

    for _ in range(epochs):
        a1.set_weights(random_weights())
        a2.set_weights(random_weights())
        game = Game(a1, a2, size)
        win.append(game.winner.weight())
        lose.append(game.loser.weight())

    return win, lose


w, l = train()

print("Winning Weights")
for i in w:
    print(i)
print(" ")
print("Losing Weights")
for i in l:
    print(i)
