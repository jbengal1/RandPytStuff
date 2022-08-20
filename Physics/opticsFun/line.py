from math import sqrt, atan, pi
from settings import *
import numpy as np

class Line:
    def __init__(self, p1 = [WIDTH/2, HEIGHT/2], p2 = [WIDTH, HEIGHT]):
        self.p1 = p1
        self.p2 = p2
        self.length = sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)
        self.vector = np.array(self.p2) - np.array(self.p1)
        self.p1Out = False
        self.p2Out = False

        self.slope = 'inf'
        if p2[0] - p1[0] != 0:
            self.slope = (p2[1] - p1[0]) / (p2[0] - p1[0])
        
        self.y_intersection = None
        if self.slope != 'inf':
            self.y_intersection = self.p1[1] - self.slope*self.p1[0]

        # angle relative to the x-axis
        self.angle = pi/2
        if self.slope != 'inf':
            self.angle = atan(self.slope)

    def updateSlope(self):
        self.slope = 'inf'
        if self.p2[0] - self.p1[0] != 0:
            self.slope = (self.p2[1] - self.p1[0]) / (self.p2[0] - self.p1[0])

    def updateYintersection(self):
        self.y_intersection = None
        if self.slope != 'inf':
            self.y_intersection = self.p1[1] - self.slope*self.p1[0]
    
    def updateLength(self):
        self.length = sqrt((self.p2[1] - self.p1[1])**2 + (self.p2[0] - self.p1[0])**2)

    def updateAngle(self):
        # angle relative to the x-axis
        self.angle = pi/2
        if self.slope != 'inf':
            self.angle = atan(self.slope)
    
    def updateVector(self):
        self.vector = np.array(self.p2) - np.array(self.p1)

    def checkBorders(self):
        if (self.p2[0] >= WIDTH) or (self.p2[0] <= 0):
            self.p2Out = True
        else:
            self.p2Out = False
        if (self.p1[0] >= WIDTH) or (self.p1[0] <= 0):
            self.p1Out = True
        else:
            self.p1Out = False
        if (self.p2[1] >= HEIGHT) or (self.p2[1] <= 0):
            self.p2Out = True
        else:
            self.p2Out = False
        if (self.p1[1] >= HEIGHT) or  (self.p1[1] <= 0):
            self.p1Out = True
        else:
            self.p1Out = False

    def setStartpoint(self, startpoint):
        self.p1 = startpoint
        self.updateSlope()
        self.updateYintersection()
        self.updateLength()
        self.updateAngle()

    def setEndpoint(self, endpoint):
        self.p2 = endpoint
        self.updateSlope()
        self.updateYintersection()
        self.updateLength()
        self.updateAngle()

    def setTwoPoints(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.updateSlope()
        self.updateYintersection()
        self.updateLength()
        self.updateAngle()

    def rotateReltop1(self, angle):
        self.angle = angle
        self.rotateVec()
        self.p2 = list(np.array(self.p1) + self.vector)
        self.updateSlope()
        self.updateYintersection()
    
    def rotateVec(self):
        c, s = np.cos(self.angle), np.sin(self.angle)
        RotationMatrix = np.array(((c, -s), (s, c)))
        self.vector = np.dot(RotationMatrix, self.vector)

    def getLineFunction(self, x):
        return self.slope*x + self.y_intersection
