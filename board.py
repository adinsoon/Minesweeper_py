import cell
from random import randint
from enum import Enum


class GameMode(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3


class Board:  # represents a field of cells

    # board has following attributes:
    # size of height and width (row, col)
    # game modes which set the number of bombs on the board
    # board will have following action methods:
    # (utility) getters
    # (user) toggle flag
    # (user) reveal field
    # (utility) count neighbours -> then set value for each cell
    # (utility) display board in debug mode (everything revealed)

    def __init__(self, height, width, mode):
        self.cells = [[cell.Cell(i, j) for i in range(width)] for j in range(height)]
        self.resolution = [height, width]
        self.mode = mode
        self.bombs_quantity = height * width

    def get_board_height(self):
        return self.resolution[0]

    def get_board_width(self):
        return self.resolution[1]

    def get_field_info(self, height, width):
        if not self.cells[height][width].is_revealed() and self.cells[height][width].has_flag():
            return 'F'
        elif not self.cells[height][width].is_revealed() and not self.cells[height][width].has_flag():
            return '_'
        elif self.cells[height][width].is_revealed() and self.cells[height][width].has_bomb():
            return 'x'
        elif self.cells[height][width].is_revealed():
            return ' '

    def debug_display(self):
        for i in range(self.get_board_height()):
            for j in range(self.get_board_width()):
                if self.cells[i][j].has_bomb():
                    print("M", end=" ")
                else:
                    print(".", end=" ")
                if self.cells[i][j].is_revealed():
                    print("o", end=" ")
                else:
                    print(".", end=" ")
                if self.cells[i][j].has_flag():
                    print("f  ", end=" ")
                else:
                    print(".  ", end=" ")
            print()

    def set_mode(self):
        if self.mode == GameMode.EASY.name:
            self.bombs_quantity = int(self.bombs_quantity * 0.1)

        elif self.mode == GameMode.NORMAL.name:
            self.bombs_quantity = int(self.bombs_quantity * 0.2)

        elif self.mode == GameMode.HARD.name:
            self.bombs_quantity = int(self.bombs_quantity * 0.3)

    def get_positions(self):
        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                print(self.cells[i][j].get_position(), end=" ")
            print()



