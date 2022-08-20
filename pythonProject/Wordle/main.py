from wordle_grid import define_grid
from wordle_button import *
from wordle_runManage import run
from wordle_keyboard import *

# Initialization
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


def main():
    # Define the grid
    grid = define_grid()

    # Define the grid
    keyboard = define_keyboard()

    # Main loop
    run(screen, grid, keyboard)


if __name__ == "__main__":
    main()
