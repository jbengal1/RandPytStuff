import pygame.time, pygame.display
from wordle_colors import *
from wordle_userInput import check_user_input
from wordle_actionManage import manage_action
from wordle_globalVar import *


def run(screen, grid, keyboard):
    """ This is the main loop function"""

    # Define the game's clock
    clock = pygame.time.Clock()
    win = False
    while not win:
        clock.tick(120)
        screen.fill(BLACK)
        key_pressed = check_user_input()
        win = manage_action(key_pressed, grid, keyboard)
        grid.draw(screen)
        keyboard.draw(screen)
        pygame.display.update()

    font = pygame.font.SysFont('Ariel', 50)
    text1 = font.render("YOU WIN!!!", 1, WHITE)
    text2 = font.render(f'On attempt {grid.line+1}/6', 1, WHITE)
    textRect1 = text1.get_rect()
    textRect1.center = (SCREEN_WIDTH / 2, 100)
    textRect2 = text2.get_rect()
    textRect2.center = (SCREEN_WIDTH / 2, 100+ 40)
    print("YOU WIN!!!")

    while True:
        clock.tick(120)
        key_pressed = check_user_input()
        screen.fill(BLACK)
        grid.draw(screen)
        keyboard.draw(screen)
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)
        pygame.display.update()
