from circle import Circle
from line import Line
from math import *

circle = Circle(position=[0,0], radius=1)
line = Line(p1=[-10, 0.5], p2=[10, 0.5])

cross_point = circle.getCrossPoint(line)
print("cross_point", cross_point)