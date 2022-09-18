import pygame
from pygame.locals import *
from settings import *
from shapes import Shapes
from math import pi
from colors import *
from hitManager import HitManager

hitManager = HitManager()

class Sim1():
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.shapes = Shapes
        self.first_Mclick = False
        self.reflected_num = 0

    def moveLinebyMouse(self):
        mouse_pos = pygame.mouse.get_pos()
        self.shapes["laser"][0].setEndpoint(mouse_pos)
    
    def setPointByMouse(self):
        mouse_pos = pygame.mouse.get_pos()
        self.shapes["laser"][0].setStartpoint(mouse_pos)
        self.first_Mclick = True

    def draw_shape(self, shape_type, shape):
        if shape_type == "laser":
            pygame.draw.line(self.display_surface, shape.color , shape.p1, shape.p2, shape.thickness)
        if shape_type == "mirror_line":
            pygame.draw.line(self.display_surface, WHITE, shape.p1, shape.p2, shape.thickness)
            pygame.draw.line(self.display_surface, BRIGHT_GRAY, shape.back_line.p1, shape.back_line.p2, shape.back_thickness)
        if shape_type == "mirror_circle":
            pygame.draw.circle(self.display_surface, WHITE, shape.position, shape.radius)
            pygame.draw.circle(self.display_surface, BRIGHT_GRAY, shape.position, shape.radius - shape.back_thickness)
            # pygame.draw.line(self.display_surface, WHITE, shape.tangent.p1, shape.tangent.p2, shape.tangent.thickness)
            # pygame.draw.line(self.display_surface, BRIGHT_GRAY, shape.tangent.back_line.p1, shape.tangent.back_line.p2, shape.tangent.back_thickness)

    def draw_shapes(self):
        for shape_type in self.shapes:
            for shape in self.shapes[shape_type]:
                self.draw_shape(shape_type, shape)
                shape.drawCoordinates(self.display_surface)

    def run(self):
        # if mouse is pressed again, reset source of light position
        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.setPointByMouse()

        # if mouse is moving, calculate laser track
        rel_mouse = pygame.mouse.get_rel()
        mouse_moved = (rel_mouse[0] != 0) or (rel_mouse[1] != 0)
        if mouse_moved:
            print(pygame.mouse.get_pos())

            # Calculate positions and interactions before drawing
            self.reflected_num = hitManager.calculateReflected(self.shapes, self.reflected_num)
            
        # draw all shapes
        self.draw_shapes()

        