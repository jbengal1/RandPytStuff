import pygame
from settings import *

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
FONT_SIZE = 14

class Text:
    def __init__(self, text='', x=WIDTH/2, y=HEIGHT/2, color=white, font_settings=('freesansbold.ttf', FONT_SIZE)):
        self.text = text
        self.font = pygame.font.Font(font_settings[0], font_settings[1])
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        self.text = self.font.render(str(self.text), True, self.color, None)
        textRect = self.text.get_rect()
        textRect.center = (self.x, self.y + 10)
        screen.blit(self.text, textRect)


class Coordinates(Text):
    def __init__(self, x=WIDTH/2, y=HEIGHT/2, color=white, font_settings=('freesansbold.ttf', FONT_SIZE)):
        super().__init__('', x, y, color, font_settings)
        self.text = '({:.2f},  '.format(self.x) + '{:.2f})'.format(self.y)

    def update(self, x, y):
        self.x = x
        self.y = y
        self.text = f'{self.x}, {self.y}'