from board import Board
import text_view as view
import text_controller as ctrl
from pygame_control import window_display

# available to change but it will also affect the size of the window and difficulty level!
# difficulty levels - "EASY", "NORMAL", "HARD"
board = Board(15, 15, "EASY")
view = view.TextView(board)

# ctrl.play(board)
# view.display()
window_display(board)
