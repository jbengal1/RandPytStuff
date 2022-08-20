import random

import numpy as np
from wordle_colors import *
from wordle_button import Button
from wordle_globalVar import *
import string
from random import randint

import enchant
import requests

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()
WORDS = [word.decode("utf-8") for word in WORDS]
englishUS_dict = enchant.Dict("en_US")


class Grid:
    buttons: list
    positions: np.array
    line: int
    col: int

    def __init__(self, arr_size, position, unit_size, margin_size):
        self.position = position
        self.arr_size = arr_size
        self.unit_size = unit_size
        self.margin_size = margin_size
        self.line = 0
        self.col = 0
        self.backSpace = False
        self.write = False
        self.allow_nextLine = False
        self.word = ''
        self.goal_word = ''
        self.win = False
        self.message = ''

    def init_grid(self, randomMyGrid=False, init_arr=[]):
        x_0, y_0 = self.position[0], self.position[1]
        N, M = self.arr_size[0], self.arr_size[1]
        l_x, l_y = self.unit_size[0], self.unit_size[1]
        self.positions = np.array([[[0, 0]]*M]*N)
        self.buttons = []
        for i in range(N):
            self.buttons.append([])
            for j in range(M):
                x = x_0 + (l_x + self.margin_size) * j
                y = y_0 + (l_y + self.margin_size) * i
                self.positions[i, j] = [x, y]
                if randomMyGrid:
                    l = list(string.ascii_lowercase)[randint(0, 24)]
                elif init_arr:
                    l = init_arr[i][j]
                else:
                    l = ""
                self.buttons[i].append(Button(WHITE, [x, y], [l_x, l_y], active=0, num=N*i+j, letter=l))

    def chose_goal_word(self):
        found_one = False
        word = ''
        search_count = 0
        while not found_one:
            print(f'Searching for goal word {search_count}/10000')
            word = random.choice(WORDS)
            if len(word) == 5:
                found_one = englishUS_dict.check(word)
            search_count += 1

        self.goal_word = word
        print('Goal word is: ', self.goal_word)

    def draw(self, window):
        for row in self.buttons:
            for button in row:
                button.draw(window)

    def write_letter(self, letter):
        i, j = self.line, self.col
        self.buttons[i][j].update_text(letter)
        self.write = True

    def delete_letter(self):
        i, j = self.line, self.col
        self.buttons[i][j].update_text("")
        self.backSpace = True

    def check_word_to_goal(self):
        if self.word == self.goal_word:
            self.win = True

        return self.win

    def manage_position(self):
        if (self.col + 1 < self.arr_size[1]) and self.write:
            self.col += 1
            self.write = False

        elif (self.col - 1 >= 0) and self.backSpace:
            self.col -= 1
            self.backSpace = False

    def check_letters(self):
        letters_status = {"correct_place": [], "wrong_place": [], "wrong_letter": []}
        for i, button in enumerate(self.buttons[self.line]):
            print(i, "coloring")
            letter = button.get_text()
            if letter == self.goal_word[i]:
                self.buttons[self.line][i].set_color(MY_GREEN)
                letters_status["correct_place"].append(letter)
            elif letter in self.goal_word:
                self.buttons[self.line][i].set_color(MY_YELLOW)
                letters_status["wrong_place"].append(letter)
            else:
                self.buttons[self.line][i].set_color(MY_GRAY)
                letters_status["wrong_letter"].append(letter)
        return letters_status

    def check_word_valid(self):
        for button in self.buttons[self.line]:
            self.word += button.get_text()

        if (len(self.word) == 5) and (englishUS_dict.check(self.word)):
            self.allow_nextLine = True
        else:
            self.message = 'Not a valid word'
            self.word = ''

    def move_line(self):
        if self.allow_nextLine:
            self.col = 0
            self.line += 1
            self.allow_nextLine = False
            self.word = ''
            # self.color_lines(MY_GRAY)

    def color_lines(self, color):
        for i, button in enumerate(self.buttons[self.line]):
            self.buttons[self.line][i].set_color(color)

    def __str__(self):
        return f'{self.positions}'


def define_grid():
    """ Define the grid """
    SIZE = 5
    grid_size, unit_size, margin_size = [SIZE, SIZE], [80, 80], 5
    gridX_length = unit_size[0] * grid_size[0] + margin_size * (grid_size[0] - 1)
    gridY_length = unit_size[1] * grid_size[1] + margin_size * (grid_size[1] - 1)
    grid_pos = [int((SCREEN_WIDTH - gridX_length) / 2), int((SCREEN_HEIGHT - gridY_length) / 2)]
    grid = Grid(grid_size, grid_pos, unit_size, margin_size)

    grid.init_grid()
    grid.chose_goal_word()

    return grid
