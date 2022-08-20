import numpy as np


class IterMixin(object):
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

class Particle(IterMixin):
    mass: float
    shape: str
    position: np.array
    velocity: np.array
    acceleration: np.array
    momentum: np.array
    kinetic: np.array
    colide: bool

    def __init__(self, shape, init_position, init_velocity, init_acceleration):
        self.mass = 1
        self.shape = shape
        self.position = np.array(init_position)
        self.velocity = np.array(init_velocity)
        self.acceleration = np.array(init_acceleration)

        self.momentum = self.mass*self.velocity
        self.mom_x = self.momentum[0]
        self.mom_y = self.momentum[1]

        self.kinetic = 0.5*self.mass*self.velocity**2
        self.kin_x = self.kinetic[0]
        self.kin_y = self.kinetic[1]

        self.pos_x = init_position[0]
        self.pos_y = init_position[1]
        self.vel_x = init_velocity[0]
        self.vel_y = init_velocity[1]
        self.accel_x = init_acceleration[0]
        self.accel_y = init_acceleration[1]

        self.colide = True

    def __str__(self):
        return str(dict(self))
   
    def set_pos(self, pos):
        self.position = pos
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def set_vel(self, vel):
        self.velocity = vel
        self.vel_x = vel[0]
        self.vel_y = vel[1]

    def set_accel(self, accel):
        self.acceleration = accel
        self.accel_x = accel[0]
        self.accel_y = accel[1]

    def set_colide(self, colide):
        self.colide = colide

    def update_mom(self, mom):
        if type(mom) == list:
            self.momentum = np.array(mom)
        elif type(mom) == np.array:
            self.momentum = mom
        else:
            print("Inavlid momentum value")

        self.mom_x = self.momentum[0]
        self.mom_y = self.momentum[1]

    def update_kinetic(self, kin):
        if type(kin) == list:
            self.kinetic = np.array(kin)
        elif type(kin) == np.array:
            self.kinetic = kin
        else:
            print("Inavlid kinetic energy value")

        self.kin_x = self.kinetic[0]
        self.kin_y = self.kinetic[1]

    def get_pos(self):
        return self.position
    
    def get_posX(self):
        return self.x

    def get_posY(self):
        return self.y

    def get_vel(self):
        return self.velocity
    
    def get_velX(self):
        return self.vel_x
    
    def get_velY(self):
        return self.vel_y

    def get_accel(self):
        return self.acceleration
    
    def get_accelX(self):
        return self.accel_x

    def get_accelY(self):
        return self.accel_y

    def move(self):
        self.position += self.velocity