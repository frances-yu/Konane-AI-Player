# Player.py
# Superclass for Human and AI

from abc import ABC, abstractmethod
from Gameboard import Gameboard


class Player(ABC):
    def __init__(self, name, is_top_left):
        self.name = name
        self.is_top_left = is_top_left

    def __str__(self):
        return self.name

    @abstractmethod
    def get_move(self, board: Gameboard):
        pass
