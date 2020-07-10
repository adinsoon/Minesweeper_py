import cell
from enum import Enum
from random import randint
from array import *


class GameMode(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3


class Board:  # represents a field of cells

    # board has following attributes:
    # size of height and width (row, col)
    # potentially a game mode which sets the number of bombs on the board
    # board will have following action methods:
    # (user) toggle flag
    # (user) reveal field
    # (utility) getters
    # (utility) count neighbours -> then set value for each cell
    # (utility) display board in debug mode (everything revealed)

    def __init__(self, height, width, mode):
        self.cells = []
        self.resolution = [height, width]
        self.mode = mode
        self.bombs_quantity = height * width

        for x in range(height):
            for y in range(width):
                self.cells.append(cell.Cell(x, y))

    def debug_display(self):
        for i in range(len(self.cells)):
            if i > 0 and i % self.resolution[1] == 0:
                print()
            if not self.cells[i].is_revealed():
                print("-", end=" ")
            elif self.cells[i].has_bomb():
                print("X", end=" ")
            elif self.cells[i].has_flag():
                print("F", end=" ")

    def set_mode(self):
        if self.mode == GameMode.EASY.name:
            self.bombs_quantity = int(self.bombs_quantity * 0.1)

        elif self.mode == GameMode.NORMAL.name:
            self.bombs_quantity = int(self.bombs_quantity * 0.2)

        elif self.mode == GameMode.HARD.name:
            self.bombs_quantity = int(self.bombs_quantity * 0.3)
