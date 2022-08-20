import GLOBALS

VOL = GLOBALS.get_volume()
N = GLOBALS.get_particle_number()

def wall_collisions(particle):
    if particle.colide:
        v = particle.get_velocity()
        
        if particle.get_posX() > VOL[0]:
            particle.set_posX(VOL[0])
            particle.set_velocity([-v[0], v[1]])
        elif particle.get_posX() < 0:
            particle.set_posX(0)
            particle.set_velocity([-v[0], v[1]])
        
        if particle.get_posY() > VOL[1]:
            particle.set_posX(VOL[1])
            particle.set_velocity([v[0], -v[1]])
        elif particle.get_posY() < 0:
            particle.set_posX(0)
            particle.set_velocity([v[0], -v[1]])