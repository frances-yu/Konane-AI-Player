# Player.py
# Superclass for Human and AI

from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @abstractmethod
    def get_move(self):
        pass
