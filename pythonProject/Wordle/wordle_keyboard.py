import numpy as np
from wordle_colors import *
from wordle_button import Button
from wordle_globalVar import *

keyboard_dic = {
    "1": ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    "2": ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
    "3": ["z", "x", "c", "v", "b", "n", "m"]
}


class Keyboard:
    buttons: list
    positions: np.array
    line: int
    col: int
    line1: []
    line2: []
    line3: []
    lines: []

    def __init__(self, position, unit_size, margin_size):
        self.position = position
        self.unit_size = unit_size
        self.margin_size = margin_size
        self.line = 0
        self.col = 0

    def init_keyboard(self):
        self.lines = [[], [], []]
        x_0, y_0 = self.position[0], self.position[1]
        l_x, l_y = self.unit_size[0], self.unit_size[1]
        for line_num, line in keyboard_dic.items():
            for i, letter in enumerate(line):
                x = x_0 + (l_x + self.margin_size) * i + 20 * int(line_num)
                y = y_0 + (l_y + self.margin_size) * int(line_num)
                self.lines[int(line_num)-1].append(Button(WHITE, [x, y], [l_x, l_y], active=0, num=i, letter=letter))

    def color_letters(self, letters_status):
        for line in self.lines:
            for button in line:
                for correct_place in letters_status["correct_place"]:
                    if correct_place == button.get_text():
                        button.set_color(MY_GREEN)
                for wrong_place in letters_status["wrong_place"]:
                    if wrong_place == button.get_text():
                        button.set_color(MY_YELLOW)
                for wrong_letter in letters_status["wrong_letter"]:
                    if wrong_letter == button.get_text():
                        button.set_color(MY_GRAY)

    def draw(self, window):
        for line in self.lines:
            for button in line:
                button.draw(window)


def define_keyboard():
    """ Define the keyboard """
    keyboard = Keyboard([1000, 1000], [40, 40], 10)
    keyboard.init_keyboard()

    return keyboard
