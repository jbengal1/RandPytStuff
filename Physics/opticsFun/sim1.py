import pygame
from settings import *
from line import Line
from rectangle import RectangleInstance

class Sim1():
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.line = Line()
        self.shapes = {
            "line": [self.line]
        }

    def moveLinebyMouse(self):
        mouse_pos = pygame.mouse.get_pos()
        self.shapes["line"][0].p1 = mouse_pos

    def draw_shape(self, shape_type, shape):
        if shape_type == "line":
            pygame.draw.line(self.display_surface, 'white', shape.p1, shape.p2, 5)

    def draw_shapes(self):
        for shape_type in self.shapes:
            for shape in self.shapes[shape_type]:
                self.draw_shape(shape_type, shape)
            
    def run(self):
        self.moveLinebyMouse()
        self.draw_shapes()


        


