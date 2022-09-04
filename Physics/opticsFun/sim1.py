import pygame
from pygame.locals import *
from settings import *
from line import Line
from light import Laser
from mirror import Mirror
from math import pi


class Sim1():
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.shapes = {
            "laser": [Laser()],
            "mirror": [Mirror()],
            "reflected": []
        }
        self.first_Mclick = False
        self.reflected = []

    def moveLinebyMouse(self):
        mouse_pos = pygame.mouse.get_pos()
        self.shapes["laser"][0].setEndpoint(mouse_pos)
    
    def setPointByMouse(self):
        mouse_pos = pygame.mouse.get_pos()
        self.shapes["laser"][0].setStartpoint(mouse_pos)
        self.first_Mclick = True

    def draw_shape(self, shape_type, shape):
        if shape_type == "laser":
            pygame.draw.line(self.display_surface, 'red', shape.p1, shape.p2, shape.thickness)
        if shape_type == "mirror":
            pygame.draw.line(self.display_surface, 'white', shape.p1, shape.p2, shape.thickness)
            pygame.draw.line(self.display_surface, 'gray', shape.back_line.p1, shape.back_line.p2, shape.back_thickness)
        if shape_type == "reflected":
            pygame.draw.line(self.display_surface, 'red', shape.p1, shape.p2, shape.thickness)

    def draw_shapes(self):
        for shape_type in self.shapes:
            for shape in self.shapes[shape_type]:
                self.draw_shape(shape_type, shape)
                shape.drawCoordinates(self.display_surface)
    
    def calculateReflected(self):
        # Clear previous reflected laser rays
        self.shapes["reflected"] = []

        # Find all reflected lasers
        for laser in self.shapes["laser"]:
            for mirror in self.shapes["mirror"]:
                laser.findEndpoint()
                # self.reflected.append( mirror.reflect(laser) )
                reflected = mirror.reflect(laser)
                if reflected is not None:
                    self.shapes["reflected"].append( reflected )


    def run(self):
        # if mouse is pressed again, reset source of light position
        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.setPointByMouse()

        # if mouse is moving, calculate laser track
        rel_mouse = pygame.mouse.get_rel()
        mouse_moved = (rel_mouse[0] != 0) or (rel_mouse[1] != 0)
        if mouse_moved:
            print(pygame.mouse.get_pos())
            print("angle*(180/pi), slope", self.shapes["laser"][0].angle*(180/pi), self.shapes["laser"][0].slope)

            # Calculate positions and interactions before drawing
            self.calculateReflected()

        # draw all shapes
        self.draw_shapes()

        