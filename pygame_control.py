import pygame as py
import board

py.font.init()
font = py.font.SysFont('Arial Black', 18)
Clock = py.time.Clock()

# available to change but it will also affect the size of the window!
cell_size = 35


def window_display(board_dest):
    first_click = 0
    delta = 0
    board_tab = board_dest

    # set position of window starting
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)

    # scalable window
    ui = 150
    height = cell_size * board_tab.get_board_height() + ui
    width = cell_size * board_tab.get_board_width()

    surface = py.display.set_mode((height, width))
    screen = py.display.get_surface()
    py.display.set_caption('Play Minesweeper!')

    running = True
    start = True

    while running:

        dt = Clock.tick() / 1000
        delta += dt
        first_click += dt

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            if event.type == py.MOUSEBUTTONDOWN and board_tab.get_game_state() == board.GameState.RUNNING.name:
                # reveal field
                if py.mouse.get_pressed()[0]:  # check if left mouse button
                    pos = py.mouse.get_pos()
                    row = int(pos[0] / cell_size)
                    col = int(pos[1] / cell_size)
                    board_tab.reveal_field(row, col)
                # toggle flag
                elif py.mouse.get_pressed()[2]:  # check if right mouse button
                    pos = py.mouse.get_pos()
                    row = int(pos[0] / cell_size)
                    col = int(pos[1] / cell_size)
                    board_tab.toggle_flag(row, col)
            # play again
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE and (board_tab.get_game_state() != board.GameState.RUNNING.name):
                    board_tab.reload_board()
                    delta = 0
                    first_click = 0
                    start = True

        surface.fill((102, 204, 255))
        field_display(board_tab, surface)

        # first reveal will start the timer
        if board_tab.revealed > 0:
            if start:
                delta -= first_click
                start = False
            draw_text(surface, "{}".format(int(delta)),
                      (board_tab.get_board_height() * cell_size + 63, (width / 10 * 2)))

        if board_tab.get_game_state() != board.GameState.RUNNING.name:
            if board_tab.get_game_state() == board.GameState.WIN.name:
                screen.fill(py.Color("black"))
                py.draw.rect(surface, (255, 220, 0), (0, 0, height, width))
                draw_text(surface, "You win!", ((height / 2) - cell_size, width / 2.75))

            if board_tab.get_game_state() == board.GameState.LOSS.name:
                screen.fill(py.Color("black"))
                py.draw.rect(surface, (100, 50, 50), (0, 0, height, width))
                draw_text(surface, "You lost!", ((height / 2) - cell_size, width / 2.75))

            draw_text(surface, "Press Space to play again", ((height / 2) - 3 * cell_size, width / 2.25))

        py.display.flip()


def field_display(board_dest, surface):
    board_tab = board_dest
    height = board_tab.get_board_height()*cell_size
    width = board_tab.get_board_width()*cell_size

    for i in range(board_tab.get_board_height()):
        for j in range(board_tab.get_board_width()):

            # not revealed and not flag
            if board_tab.get_field_info(i, j) == '_':
                py.draw.rect(surface, (192, 192, 192), (0 + i * cell_size, 0 + j * cell_size, cell_size, cell_size))

            # not revealed and got flag
            elif board_tab.get_field_info(i, j) == 'F':
                py.draw.rect(surface, (255, 200, 150), (0 + i * cell_size, 0 + j * cell_size, cell_size, cell_size))

            # revealed and got bomb
            elif board_tab.get_field_info(i, j) == 'x':
                py.draw.rect(surface, (255, 0, 0), (0 + i * cell_size, 0 + j * cell_size, cell_size, cell_size))
                py.draw.circle(surface, (0, 0, 0), (20 + i * cell_size, 20 + j * cell_size), int(cell_size / 3))

            # revealed and no neighbours
            elif board_tab.get_field_info(i, j) == ' ':
                py.draw.rect(surface, (224, 224, 224), (0 + i * cell_size, 0 + j * cell_size, cell_size, cell_size))

            # revealed and got neighbours
            else:
                py.draw.rect(surface, (224, 224, 224), (0 + i * cell_size, 0 + j * cell_size, cell_size, cell_size))
                draw_text(surface, str(board_tab.count_neighbours(i, j)),
                          (cell_size / 3 + i * cell_size, cell_size / 6 + j * cell_size))

    # lines to separate each cell
    for i in range(1, board_tab.get_board_width() + 1):
        py.draw.line(surface, (0, 102, 204), (0, i * cell_size),
                     (height, i * cell_size))
    for i in range(1, board_tab.get_board_height() + 1):
        py.draw.line(surface, (0, 102, 204), (i * cell_size, 0),
                     (i * cell_size, width))

    draw_text(surface, "Bombs:", (height + 40, (width / 10 * 4)))
    draw_text(surface, "{}".format(board_tab.bombs_quantity), (height + 60, (width / 10 * 5)))

    draw_text(surface, "Flags:", (height + 45, (width / 10 * 7)))
    draw_text(surface, "{}".format(board_tab.toggled), (height + 65, (width / 10 * 8)))

    draw_text(surface, "Time:", (height + 50, (width / 10 * 1)))


def draw_text(surface, label, position):
    subtext = font.render(label, False, (0, 0, 0))
    surface.blit(subtext, (position[0], position[1]))
