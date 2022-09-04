from settings import *
from line import Line


class Wall(Line):
    def __init__(self, p1 = [WIDTH/2, HEIGHT/2], p2 = [WIDTH, HEIGHT], name = "wall"):
        super().__init__(p1, p2, name)
        self.obsticle = False


WALL_UP = Wall([0, 0], [WIDTH, 0], name="wall_up")
WALL_DOWN = Wall([0, HEIGHT], [WIDTH, HEIGHT], name="wall_down")
WALL_LEFT = Wall([0, 0], [0, HEIGHT], name="wall_left")
WALL_RIGHT = Wall([WIDTH, 0], [WIDTH, HEIGHT], name="wall_right")
WALLS = [WALL_UP, WALL_DOWN, WALL_LEFT, WALL_RIGHT]