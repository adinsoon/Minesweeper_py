import numpy as num


class Cell:  # represents one single cell on the board

    # each cell may have the following attributes:
    # has bomb or not
    # has flag or not
    # has been revealed or not
    # each cell has it own position on the board
    # cell may show its neighbours if it doesn't have a bomb and is revealed simultaneously

    def __init__(self, x_row, y_col):
        self.x = x_row
        self.y = y_col
        self.position = [self.x, self.y]
        self.has_cell_bomb = False
        self.has_cell_flag = False
        self.is_cell_revealed = False
        self.value = int
        self.string = "A"

    def toggle_flag(self):
        self.has_cell_flag = num.invert(self.has_cell_flag)

    def reveal_field(self):
        self.is_cell_revealed = num.invert(self.is_cell_revealed)

    def put_bomb(self):
        self.has_cell_bomb = num.invert(self.has_cell_bomb)

    def has_bomb(self):
        return self.has_cell_bomb

    def has_flag(self):
        return self.has_cell_flag

    def is_revealed(self):
        return self.is_cell_revealed

    def set_value(self, value):
        self.value = value

    def get_position(self):
        return self.position

    def get_value(self):
        return self.value

    def get_string(self):
        return self.string
