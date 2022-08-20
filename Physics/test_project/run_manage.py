import numpy as np
import matplotlib.pyplot as plt

import GLOBALS

VOL = GLOBALS.get_volume()
N = GLOBALS.get_particle_number()
TIME = GLOBALS.get_time()

class Run:
    def __init__(self):
        self.x = []
        self.y = []

    def run(self, particles):
        for t in TIME:
            for particle in particles.particles_array:
                self.x.append(particle.pos_x)
                self.y.append(particle.pos_y)
            particles.move()

    def plot(self):
        plt.scatter(self.x, self.y)
        plt.show()