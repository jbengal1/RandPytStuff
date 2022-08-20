import pygame
from settings import *
from line import Line
from math import sqrt, cos, sin, acos, pi
import numpy as np
from numpy import linalg


class Laser(Line):
    def __init__(self):
        super().__init__()
        self.obsticle = False
    
    def findEndpoint(self):       
        self.setEndpoint(list(pygame.mouse.get_pos()))

        # mouseVec = np.array(pygame.mouse.get_pos())
        # mouseVecReltop1 = mouseVec - np.array(self.p1)
        # mouseRelAngle = 0
        # if (self.length !=0) and (linalg.norm(mouseVecReltop1 != 0)):
        #     mouseRelAngle = acos(np.dot(self.vector, mouseVecReltop1)/(self.length*linalg.norm(mouseVecReltop1)))

        # print(self.vector, mouseVecReltop1)        

        # self.rotateReltop1(mouseRelAngle)

        # print("laser from", self.p1, "to", self.p2)
        # print("mouse", pygame.mouse.get_pos())
        
        iteration = 0 
        while not self.obsticle:
            iteration += 1
            dl = 10
            x2 = self.p2[0] + dl*cos(self.angle)
            y2 = self.p2[1] + dl*sin(self.angle)
            self.setEndpoint([x2 ,y2])

            self.checkBorders()
            # print(iteration, self.p2Out, self.p2)
            if self.p2Out or (iteration>100):
                break
            



class Spotlight(Line):
    pass


def test():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    laser = Laser()
    print(laser.p2)


    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_x]):
                pygame.quit()
                sys.exit()
        
        rel_mouse = pygame.mouse.get_rel()

        if (rel_mouse[0] != 0) and (rel_mouse[1] != 0):
            laser.findEndpoint()

        # Draw on screen
        screen.fill('black')
        pygame.draw.line(screen, 'white', laser.p1, laser.p2, 5)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    import sys
    test()