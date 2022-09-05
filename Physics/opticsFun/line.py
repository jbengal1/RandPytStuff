from math import sqrt, acos, atan, pi
from settings import *
import numpy as np
from numpy.linalg import norm
import json
import text

LINE_THICKNESS = 3

class Line:
    def __init__(self, p1 = [WIDTH/2, HEIGHT/2], p2 = [WIDTH/4, HEIGHT], name="defultLine"):
        self.name = name

        self.p1 = p1
        self.p2 = p2
        self.length = sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)
        self.thickness = LINE_THICKNESS
        self.vector = np.array(self.p2) - np.array(self.p1)
        self.p1Out = False
        self.p2Out = False
        self.draw_coordinates = False
        
        self.slope = 'inf'
        if p2[0] - p1[0] != 0:
            self.slope = (p2[1] - p1[1]) / (p2[0] - p1[0])

        self.y_intersection = None
        if self.slope != 'inf':
            self.y_intersection = self.p1[1] - self.slope*self.p1[0]

        # angle relative to the x-axis
        self.angle = pi/2
        if self.slope != 'inf':
            if self.vector[1] != 0:
                self.angle = atan(self.vector[1]/self.vector[0])
    
    def __str__(self):
        self.directory = {
            "name": self.name, 
            "p1": self.p1, "p2": self.p2,
            "vector": list(self.vector),
            "p1Out": self.p1Out, "p2Out": self.p2Out,
            "slope": self.slope, "y_intersection": self.y_intersection,
            "angle": self.angle
            }
        return json.dumps(self.directory, indent=4)

    def updateSlope(self):
        self.slope = 'inf'
        if (self.p2[0] - self.p1[0] > 0) or (self.p2[0] - self.p1[0] < 0):
            self.slope = (self.p2[1] - self.p1[1]) / (self.p2[0] - self.p1[0])

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
            if self.vector[1] != 0:
                self.angle = atan(self.vector[1]/self.vector[0])
                if self.angle < 0:
                    self.angle += pi

    def updateVector(self):
        self.vector = np.array(self.p2) - np.array(self.p1)
    
    def updateAll(self):
        self.updateVector()
        self.updateSlope()
        self.updateYintersection()
        self.updateLength()
        self.updateAngle()
        
        
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
        self.updateAll()

    def setEndpoint(self, endpoint):
        self.p2 = endpoint
        self.updateAll()

    def setTwoPoints(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.updateAll()

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
        # Calcualte the y coordinate
        return self.slope*x + self.y_intersection
        
    def checkPointOn(self, point):
        # Check if the calculated point inside the finite line
        on = False
        rel_vec = np.array(point) - np.array(self.p1)
        rel_angle = self.relAngleVec(rel_vec)
        if norm(rel_vec) <= norm(self.vector) and rel_angle <= 0.0001:
            on = True
        return on
            
    def getCrossPoint(self, line2):
        # the function returns the [x,y] cross between two finite lines,
        # if it exists, and None otherwise.
        if self.slope == line2.slope or self.length == 0:
            return None        
        else:
            # Calculate cross point (assuming infinite lines)
            if self.slope == 'inf':
                x_cross = self.p1[0]
                y_cross = line2.getLineFunction(x_cross)
            else:
                if line2.slope == 'inf':
                    x_cross = line2.p1[0]
                else:
                    x_cross = -(self.y_intersection - line2.y_intersection)/(self.slope - line2.slope)
                y_cross = self.getLineFunction(x_cross)

            # checking if the point found is inside the boundries of each line
            if y_cross != None:
                if self.checkPointOn([x_cross, y_cross]) and line2.checkPointOn([x_cross, y_cross]):
                    return [x_cross, y_cross]
                else:
                    return None
            else:
                return None

    def relAngleLine(self, line2):
        vec1 = self.vector
        vec2 = line2.vector
        dot = np.dot(vec1, vec2)

        # Fix errors due to floating point
        if dot < -1:
            dot = -1
        elif dot > 1:
            dot = 1
        return acos( dot / (norm(vec1)*norm(vec2)) )
    
    def relAngleVec(self, vec2):
        vec1 = self.vector
        v1_direction = vec1/norm(vec1)
        v2_direction = vec2/norm(vec2)
        dot = np.dot(v1_direction, v2_direction)
        
        # Fix errors due to floating point
        if dot < -1:
            dot = -1
        elif dot > 1:
            dot = 1
        return acos( dot )

    def drawCoordinates(self, screen, draw=True):
        self.draw_coordinates = draw

        if self.draw_coordinates:
            # Create text objects
            self.text_coordiantes1 = text.Coordinates(x=self.p1[0], y=self.p1[1])
            self.text_coordiantes2 = text.Coordinates(x=self.p2[0], y=self.p2[1])

            # Draw text objects on the screen
            self.text_coordiantes1.draw(screen)
            self.text_coordiantes2.draw(screen)


    def checkAbovePoint(self, point):
        # This method takes a given point and
        # check wether its below the line function
        a, b = self.slope, self.y_intersection
        if a >= 0:
            if (point[0] >= b/a - point[1]/a) and (point[1] <= a*point[0] + b):
                return True
            else:
                return False
        else:
            if (point[0] <= b/a - point[1]/a) and (point[1] <= a*point[0] + b):
                return True
            else:
                return False
            
        
    def calculateDistanceTo(self, point):
        m = self.slope
        n = self.y_intersection
        x = point[0]
        y = point[1]
        return abs((m*x - y + n)/sqrt(m**2 + 1))