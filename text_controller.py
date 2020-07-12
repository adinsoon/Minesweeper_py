
# simple function allowing to play text version of the game
# note: use it together with text_view function in while loop


def play(board_tab):
    # numeration starts from 0
    print(board_tab.get_board_height())
    upper_range_height = int(board_tab.get_board_height())
    upper_range_height -= 1
    upper_range_width = int(board_tab.get_board_width())
    upper_range_width -= 1

    good_answer = False

    while not good_answer:
        print("Choose your action from the list below:")
        print("'1' - Reveal field")
        print("'2' - Toggle flag")
        answer = input()

        # reveal field
        if answer == "1":

            good_answer_row = False
            while not good_answer_row:
                print("Choose row from 0 to {}:".format(upper_range_height))
                row = input()
                try:
                    if 0 <= int(row) <= board_tab.get_board_height():
                        good_answer_row = True
                    else:
                        print("Invalid value. Please try again.")
                except ValueError:
                    print("Invalid value. Please try again.")

            good_answer_col = False
            while not good_answer_col:
                print("Choose column from 0 to {}:".format(upper_range_width))
                col = input()
                try:
                    if 0 <= int(col) <= board_tab.get_board_width():
                        good_answer_col = True
                    else:
                        print("Invalid value. Please try again.")
                except ValueError:
                    print("Invalid value. Please try again.")
            row = int(row)
            col = int(col)
            board_tab.reveal_field(row, col)
            good_answer = True

        # toggle flag
        elif answer == "2":

            good_answer_row = False
            while not good_answer_row:
                print("Choose row from 0 to {}:".format(upper_range_height))
                row = input()
                try:
                    if 0 <= int(row) <= board_tab.get_board_height():
                        good_answer_row = True
                    else:
                        print("Invalid value. Please try again.")
                except ValueError:
                    print("Invalid value. Please try again.")
            good_answer_col = False

            while not good_answer_col:
                print("Choose column from 0 to {}:".format(upper_range_width))
                col = input()
                try:
                    if 0 <= int(col) <= board_tab.get_board_width():
                        good_answer_col = True
                    else:
                        print("Invalid value. Please try again.")
                except ValueError:
                    print("Invalid value. Please try again.")
            row = int(row)
            col = int(col)
            board_tab.toggle_flag(row - 1, col - 1)
            good_answer = True

        else:
            print("Invalid action. Try again.")
