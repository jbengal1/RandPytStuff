from settings import *
from line import Line, LINE_THICKNESS
from circle import Circle
from light import Laser
from math import pi, sqrt
import numpy as np
from numpy.linalg import norm
from vector_functions import rotateVec2d


class Mirror():
    def __init__(self, name = "general_mirror"):
        super(Mirror, self).__init__()
        print("self.name = " + name)
        self.name = name
        self.cross_point = None
        self.one_sided = True

    def __str__(self):
        return self.name


class MirrorLine(Line, Mirror):
    def __init__(self, p1 = [2*WIDTH/6, 2*HEIGHT/4], p2 = [5*WIDTH/2, 5*HEIGHT/3], name = "linear_mirror"):
        super(MirrorLine, self).__init__(p1, p2, name)
        self.middle = [self.p2[0] -self.p1[0], self.p2[1] - self.p1[1]]
        self.back_thickness = 2*self.thickness
        self.back_line = backSideLine(self)
    
    def backToPoint(self, point):
        dist_to_mirror = self.calculateDistanceTo(point)
        dist_to_back = self.back_line.calculateDistanceTo(point)
        if dist_to_mirror > dist_to_back:
            return True
        else:
            return False            
    
    def reflect(self, light, cross_point=None):

        if cross_point is None: self.cross_point = self.getCrossPoint(light)
        else: self.cross_point = cross_point

        flag = True
        if self.one_sided: flag = not self.backToPoint(light.p1)
        print("self.cross_point", self.cross_point)
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
            reflected_light = Laser(self.cross_point, list(reflect_dirc_endpoint), name = "reflected")
            reflected_light.reflected = True
            reflected_light.findEndpoint()

            # Short the original to it's crosspoint
            light.setEndpoint(self.cross_point)

            # return the reflected light
            return reflected_light

class MirrorCircle(Circle, Mirror):
    def __init__(self, radius=10, position=[WIDTH/2, HEIGHT/2]):
        super(MirrorCircle, self).__init__(radius=radius, position=position)
        self.back_thickness = 2*LINE_THICKNESS
        self.cross_point = None
        self.tangent = MirrorLine(p1=[0,0], p2=[1,1], name="tangent")

    def pointInside(self, point):
        check_vector = np.array(point) - np.array(self.position)
        if norm(check_vector) < self.radius:
            return True
        else:
            return False        
    
    def updateTangent(self):
        center_vector = np.array(self.cross_point) - np.array(self.position)
        self.tangent.setStartpoint(rotateVec2d(center_vector, -pi/2) + self.cross_point)
        self.tangent.setEndpoint(rotateVec2d(center_vector, pi/2) + self.cross_point)
        self.tangent.back_line = backSideLine(self.tangent)

    def reflect(self, light):
        self.cross_point = self.getCrossPoint(light)        
        if self.cross_point != None :
            if light.checkPointOn(self.cross_point):
                self.updateTangent()
                
                # return the reflected light
                reflected_light = self.tangent.reflect(light, self.cross_point)
                return reflected_light

def backSideLine(mirror):
    prep_direction = np.array([
        mirror.direction[1], -mirror.direction[0]
        ])
    
    mirror.back_space_vec = prep_direction*mirror.back_thickness*0.8
    new_p1 = np.array(mirror.p1) + mirror.back_space_vec
    new_p2 = np.array(mirror.p2) + mirror.back_space_vec
    return Line(list(new_p1), list(new_p2))


if __name__ == '__main__':
    test_mirror = MirrorCircle()
    print(test_mirror.pointInside([601, 601]))
