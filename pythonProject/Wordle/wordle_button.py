import pygame.rect
from pygame import draw
from wordle_colors import *


def cyclic_index(i, N):
    if i == N:
        return 0
    else:
        return i


class Button:
    shape: pygame.rect

    def __init__(self, color, position, size, active, num, letter=""):
        self.color = color
        self.active = active
        self.position = position
        self.size = size
        self.shape = pygame.Rect([position, size])
        self.num = num
        self.letter = letter

        self.font = pygame.font.SysFont('Ariel', 50)

    def draw(self, window):
        draw.rect(window, self.color, self.shape)
        self.draw_text(window)

    def draw_text(self, window):
        text = self.font.render(self.letter, 1, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2)
        window.blit(text, textRect)

    def update_text(self, letter):
        self.letter = letter

    def get_text(self):
        return self.letter

    def update_color(self, color):
        self.color = color

    def set_color(self, color):
        self.color = color

    def __str__(self):
        return f'{self.text_str}'

