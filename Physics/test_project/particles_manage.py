import numpy as np

import collisions_manage
import particle_obj
import GLOBALS


VOL = GLOBALS.get_volume()
N = GLOBALS.get_particle_number()
T = GLOBALS.get_time()

class Particles(particle_obj.Particle):
    def __init__(self):
        self.particles_array= []
    
    def initState1(self):
        for i in range(N):
            
            # randomly choose 2-dim array of x, y inside the physical volume
            init_pos = VOL[1]*np.random.rand(2)
            
            # randomly choose 2-dim array of velocities in x, y between -1 to 1
            init_vel = np.random.uniform(-1, 1, 2)

            init_accel = [0, 0]
            
            # push particles to the array
            self.particles_array.append(particle_obj.Particle("square", init_pos, init_vel, init_accel)) 
    
    def move(self):
        for particle in self.particles_array:
            particle.move()