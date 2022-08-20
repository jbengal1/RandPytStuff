import pygame.key
import string


def manage_action(key, grid, keyboard):

    for letter in list(string.ascii_lowercase):
        if key == pygame.key.key_code(letter):
            grid.write_letter(letter)
            grid.manage_position()
            print(grid.line, grid.col)
            break

    if key == pygame.key.key_code("\b"):
        grid.manage_position()
        grid.delete_letter()

    elif key == pygame.key.key_code("\r"):
        grid.check_word_valid()
        if grid.check_word_to_goal():
            return True
        else:
            letters_status = grid.check_letters()
            keyboard.color_letters(letters_status)
            grid.move_line()

    else:
        pass
    # print(grid.line, grid.col)
    return False
