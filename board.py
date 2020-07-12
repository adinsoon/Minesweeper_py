import cell
from random import randint
from enum import Enum


class GameMode(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3


class GameState(Enum):
    RUNNING = 0
    WIN = 1
    LOSS = 2


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
        self.set_mines()
        self.revealed = 0
        self.toggled = 0
        self.exploded = 0
        self.free_cells = height*width - self.bombs_quantity
        self.directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]

    ''' USER ACTIONS '''

    def toggle_flag(self, x, y):
        if self.is_on_board(x, y) and not self.cells[x][y].is_revealed():
            if self.cells[x][y].has_flag():
                self.toggled -= 1
            elif not self.cells[x][y].has_flag():
                self.toggled += 1
            self.cells[x][y].toggle_flag()

    def reveal_field(self, x, y):
        """
        if its the first player action and there is a mine or is around in the 3x3 matrix - move mine(s)
        to another location, reveal 3x3 field and try to flood fill congruent area
        if it doesn't matter which one player action except first - reveal the field and try to flood fill congruent
        area every time the field is revealed, the field is counted to the counter of all revealed
        """
        if self.get_game_state() == GameState.RUNNING.name:
            if self.is_on_board(x, y) and not self.cells[x][y].has_flag() and not self.cells[x][y].is_revealed():
                if self.revealed == 0:  # first player action case
                    counter = 0
                    # check x/y position
                    if self.cells[x][y].has_bomb():
                        counter += 1
                        self.cells[x][y].take_bomb()
                    self.cells[x][y].reveal_field()
                    self.revealed += 1
                    # check fields around x/y position
                    for row, col in self.directions:
                        if self.is_on_board(x + row, y + col):
                            if self.cells[x + row][y + col].has_bomb():
                                self.cells[x + row][y + col].take_bomb()
                                counter += 1
                            self.cells[x + row][y + col].reveal_field()
                            self.revealed += 1
                    # put taken bombs into other fields
                    while counter > 0:
                        temp_x = randint(0, self.get_board_height() - 1)
                        temp_y = randint(0, self.get_board_width() - 1)
                        if not self.cells[temp_x][temp_y].has_bomb() and not self.cells[temp_x][temp_y].is_revealed():
                            self.cells[temp_x][temp_y].put_bomb()
                            counter -= 1
                    # check for flood fill availability
                    for row, col in self.directions:
                        if x + row >= 0 and y + col >= 0:
                            if self.count_neighbours(x + row, y + col) == 0:
                                self.flood_fill(x + row, y + col)
                else:  # every other next player action
                    # there is a bomb so it leads to an explosion -> game over
                    if self.cells[x][y].has_bomb():
                        self.cells[x][y].reveal_field()
                        self.exploded += 1
                    # there is no bomb so it's possible to reveal without worries then try flood fill
                    elif not self.cells[x][y].has_bomb():
                        self.cells[x][y].reveal_field()
                        self.revealed += 1
                    if self.count_neighbours(x, y) == 0:
                        self.flood_fill(x, y)

    ''' GETTERS '''

    def get_board_height(self):
        return self.resolution[0]

    def get_board_width(self):
        return self.resolution[1]

    def get_positions(self):
        print("Note: The first value is column, the second is row")
        for i in range(self.resolution[0]):
            for j in range(self.resolution[1]):
                print(self.cells[i][j].get_position(), end=" ")
            print()

    ''' BOOLEANS '''

    def is_on_board(self, x, y):
        return 0 <= x < self.get_board_height() and 0 <= y < self.get_board_width()

    def is_able_to_fill(self, x, y):
        return (self.is_on_board(x, y) and not self.cells[x][y].has_bomb() and not self.cells[x][y].has_flag()
                and not self.cells[x][y].is_revealed())

    ''' SETTERS '''

    def set_mines(self):
        # put bombs on the board to the random cells
        # how many it depends on the selected mode and size of the board
        self.set_mode()
        i = 0
        while i < self.bombs_quantity:
            x = randint(0, self.get_board_height() - 1)
            y = randint(0, self.get_board_width() - 1)
            if self.cells[x][y].has_bomb():
                pass
            else:
                self.cells[x][y].put_bomb()
                i += 1

    def set_mode(self):
        if self.mode == GameMode.EASY.name:
            self.bombs_quantity = int(self.bombs_quantity * 0.1)

        elif self.mode == GameMode.NORMAL.name:
            self.bombs_quantity = int(self.bombs_quantity * 0.2)

        elif self.mode == GameMode.HARD.name:
            self.bombs_quantity = int(self.bombs_quantity * 0.3)

        self.free_cells = self.get_board_height() * self.get_board_width() - self.bombs_quantity

    ''' OTHER '''

    def flood_fill(self, x, y):
        for row, col in self.directions:
            if x + row >= 0 and y + col >= 0:
                if self.is_able_to_fill(x + row, y + col):
                    self.reveal_field(x + row, y + col)

    def count_mines_on_board(self):
        bomb_quantity = 0
        for i in range(self.get_board_height()):
            for j in range(self.get_board_width()):
                if self.cells[i][j].has_bomb():
                    bomb_quantity += 1
        return bomb_quantity

    def count_neighbours(self, x, y):
        count = 0
        if self.is_on_board(x,y):
            if self.cells[x][y].is_revealed():
                for row, col in self.directions:
                    if x + row >= 0 and y + col >= 0:
                        if self.is_on_board(x + row, y + col):
                            if self.cells[x + row][y + col].has_bomb():
                                count += 1
        return count

    # clean and prepare for another game
    def reload_board(self):
        for i in range(self.get_board_height()):
            for j in range(self.get_board_width()):
                self.__init__(self.get_board_height(), self.get_board_width(), self.mode)

    ''' FIELD INFO '''

    def get_field_info(self, height, width):
        if not self.cells[height][width].is_revealed() and self.cells[height][width].has_flag():
            return 'F'
        elif not self.cells[height][width].is_revealed() and not self.cells[height][width].has_flag():
            return '_'
        elif self.cells[height][width].is_revealed() and self.cells[height][width].has_bomb():
            return 'x'
        elif self.cells[height][width].is_revealed() and self.count_neighbours(height, width) == 0:
            return ' '
        elif self.cells[height][width].is_revealed() and self.count_neighbours(height, width) != 0:
            return str(self.count_neighbours(height, width))

    '''' GAME INFO '''

    def get_game_state(self):
        # WIN IF all mines were flagged and there are no flags on fields without mines, or
        # WIN IF all unrevealed fields have mines
        # LOSS IF any field is revealed and has mine
        count_fields = self.free_cells
        for i in range(self.get_board_height()):
            for j in range(self.get_board_width()):
                if not self.cells[i][j].has_bomb() and self.cells[i][j].is_revealed():
                    count_fields -= 1
        if count_fields == 0:
            return GameState.WIN.name
        if self.exploded > 0:
            return GameState.LOSS.name
        else:
            return GameState.RUNNING.name

    ''' DEBUG '''

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
