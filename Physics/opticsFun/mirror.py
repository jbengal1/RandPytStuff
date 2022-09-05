from settings import *
from line import Line
from light import Laser
from math import pi, cos, sin
import numpy as np
from numpy.linalg import norm
from vector_functions import rotateVec2d

class Mirror(Line):
    def __init__(self, p1 = [2*WIDTH/6, 2*HEIGHT/4], p2 = [5*WIDTH/2, 5*HEIGHT/3], name = "mirror"):
        super().__init__(p1, p2, name)
        self.cross_point = None
        
        self.middle = [self.p2[0] -self.p1[0], self.p2[1] - self.p1[1]]
        self.back_thickness = 2*self.thickness
        self.back_line = backSideLine(self)
        self.one_sided = True
    
    def backToPoint(self, point):
        dist_to_mirror = self.calculateDistanceTo(point)
        dist_to_back = self.back_line.calculateDistanceTo(point)
        if dist_to_mirror > dist_to_back:
            return True
        else:
            return False            
    
    def reflect(self, light):
        self.cross_point = self.getCrossPoint(light)
        flag = True
        if self.one_sided: flag = not self.backToPoint(light.p1)
        if (self.cross_point != None) and (flag):
            
            # Calculte the direction vector of the reflected light            
            rel_angle = self.relAngleVec(light.vector)
            if rel_angle >= pi/2:
                rel_angle = pi - rel_angle
            else:
                rel_angle *= -1
                
            l_vector = light.vector/norm(light.vector)
            direction_vec = rotateVec2d(l_vector, 2*rel_angle)
        
            direction_vec *= 200
            reflect_dirc_endpoint = np.array(self.cross_point) + direction_vec

            # Create a new reflected light object
            reflected_light = Laser(self.cross_point, list(reflect_dirc_endpoint), name = "reflect")
            reflected_light.reflected = True
            reflected_light.findEndpoint()

            # Short the original to it's crosspoint
            light.setEndpoint(self.cross_point)

            # return the reflected light
            return reflected_light

def backSideLine(mirror):
    direction_vec = np.array(mirror.p2) - np.array(mirror.middle)
    direc = direction_vec/norm(direction_vec)
    prep_direction = np.array([direc[1], -direc[0]])
    
    mirror.back_space_vec = prep_direction*mirror.back_thickness
    new_p1 = np.array(mirror.p1) + mirror.back_space_vec
    new_p2 = np.array(mirror.p2) + mirror.back_space_vec
    return Line(list(new_p1), list(new_p2))