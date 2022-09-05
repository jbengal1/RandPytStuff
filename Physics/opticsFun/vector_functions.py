import numpy as np
from numpy.linalg import norm
from math import cos, sin

def rotateVec2d(vector, angle):
    a = vector[0]
    b = vector[1]
    t = angle
    return np.array([
        a*cos(t) + b*sin(t),
        -a*sin(t) + b*cos(t)
        ])

