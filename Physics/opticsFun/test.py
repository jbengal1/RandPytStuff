from walls import *
from math import *
from pygame.locals import *
from line import Line
import pygame, sys
from settings import *

import numpy as np

class Test:
    def __init__(self):
        
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("test")
        self.clock = pygame.time.Clock()

        self.line1 = Line([100,200], [300,100], "1")
        self.line2 = Line([300,200], [100,300], "2")

    def run(self):

        t = 0
        dt = 0.02
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[K_x]):
                    pygame.quit()
                    sys.exit()


            crossPoint = self.line1.getCrossPoint(self.line2)
            print("crossPoint", crossPoint)
            # print("1", self.line1.p1, self.line1.p2)
            # print("2", self.line2.p1, self.line2.p2)


            if crossPoint == None:
                print(crossPoint)
                crossPoint = [WIDTH/2, HEIGHT/2]
            self.screen.fill('black')
            pygame.draw.line(self.screen, 'green', self.line1.p1, self.line1.p2, 5)
            pygame.draw.line(self.screen, 'red', self.line2.p1, self.line2.p2, 5)
            pygame.draw.circle(self.screen, 'white', crossPoint, 10, 1 )
            pygame.display.flip()
            self.clock.tick(FPS)
            
            self.line1.setEndpoint(list( np.array(self.line1.p2) + t ))
            self.line2.setEndpoint(list( np.array(self.line2.p2) + t ))

            t += dt

if __name__ == "__main__":
    test = Test()
    test.run()




