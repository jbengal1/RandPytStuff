import pygame, sys
WIDTH = 500
HEIGHT = 500
FPS = 20

def draw_test(screen, angle):
    print(angle)
    stick1 = pygame.Surface((10, 90))
    stick1.fill('green')
    # stick1.set_colorkey('orange')
    stick1 = pygame.transform.rotate(stick1, angle)
    screen.blit(stick1, (20, 300))

class Test:
    def __init__(self):
        
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Test")
        self.clock = pygame.time.Clock()

    def run(self):
        angle = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            draw_test(self.screen, angle)
            pygame.display.update()
            self.clock.tick(FPS)

            angle += 1


if __name__ == "__main__":
    test = Test()
    test.run()
