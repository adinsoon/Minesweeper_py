import board

board = board.Board(10, 9, "EASY")

# for i in range(len(board.cells)):
#     print(i)
#     print(board.cells[i].get_position())

board.debug_display()
board.set_mode()
print(board.bombs_quantity)


