import pygame, sys
from settings import *
from sim1 import Sim1

class OpticSimulation:
    def __init__(self):
        
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()

        # Set the simulation I want to run
        self.sim1 = Sim1()

    def run(self):
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[K_x]):
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.sim1.run()
            pygame.display.update()
            self.clock.tick(FPS)
            print(pygame.mouse.get_pos())


if __name__ == "__main__":
    optic_sim = OpticSimulation()
    optic_sim.run()
