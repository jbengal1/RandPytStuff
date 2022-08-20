from dataclasses import dataclass
import numpy as np
import sys, pygame
from pygame import display, draw

#  Colors Palet
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

# Initialization
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


@dataclass
class Ant:
    position: list
    velocity: list
    rect: pygame.rect

    def __init__(self, position, velocity, size):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.size = np.array(size)
        self.rect = pygame.Rect([position, size])

    def __str__(self):
        return f"position: {self.position}, velocity: {self.velocity}"

    def move(self):
        self.rect = self.rect.move(self.velocity)

@dataclass
class Food:    
    position: list
    rects: list

    def __init__(self, position, grid_size):
        self.position = np.array(position)
        self.color = [255, 0, 0]
        self.grid_size = grid_size
        self.set_grid()

    def set_grid(self):
        self.rects = [[0 for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]
        self.colors = [[0 for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]
        rect_size = [10, 10]
        line_thickness = 1
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                rect_pos = self.position + np.array([i*(rect_size[0] + line_thickness) , j*(rect_size[0] + line_thickness)])
                self.rects[i][j] = pygame.Rect([rect_pos, rect_size])
                self.colors[i][j] = self.color.copy()

    def draw_grid(self, screen):
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                draw.rect(screen, self.colors[i][j], self.rects[i][j])





def set_ants(positions, velocities):
    N = len(positions)
    ant_size = [10, 10]
    return [Ant(positions[i], velocities[i], ant_size) for i in range(N)]


def check_user_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()


def manage_collisions_walls(ant):
    if ant.rect.left < 0 or ant.rect.right > SCREEN_WIDTH:
        ant.velocity[0] = -ant.velocity[0]
    if ant.rect.top < 0 or ant.rect.bottom > SCREEN_HEIGHT:
        ant.velocity[1] = -ant.velocity[1]


def manage_collisions_food(ant, food):
    pass
    # for i in range(food.grid_size[0]):
    #     for j in range(food.grid_size[1]):
    #         if ant.rect.colliderect(food.rects[i][j]):
    #             if ant.rect.left < food.rects[i][j]. or ant.rect.right > SCREEN_WIDTH:
    #                 ant.velocity[0] = -ant.velocity[0]
    #             if ant.rect.top < 0 or ant.rect.bottom > SCREEN_HEIGHT:
    #                 ant.velocity[1] = -ant.velocity[1]


def main():
    positions = [[0, 0], [10, 10],[20, 20], [30, 30], [40, 40]]
    velocities = [[1, 1], [5, 1], [-1, 3], [-2, 9], [2, 4]]
    
    ants = set_ants(positions, velocities)
    food = Food([200, 200], [10, 10])
    clock = pygame.time.Clock()

    while True:
        clock.tick(120)
        screen.fill(BLACK)

        check_user_input()
        
        for ant in ants:
            ant.move()
            manage_collisions_walls(ant)
            draw.rect(screen, BLUE, ant.rect)
        
        food.draw_grid(screen)
        pygame.display.update()


if __name__=="__main__":
    main()
