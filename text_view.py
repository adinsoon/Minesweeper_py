import board


class TextView:

    # simple task - show board according to given data

    def __init__(self, game_board):
        self.board = game_board

    def display(self):
        for i in range(self.board.get_board_height()):
            for j in range(self.board.get_board_width()):
                print(self.board.get_field_info(i, j), end=" ")
            print()


