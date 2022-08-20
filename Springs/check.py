import numpy as np

x = []
with open("frames_osc100_fra12000/frames_osc100_fra12000.txt", "r") as file:
    for line in file:
        x.append(line.split())
x = np.array(x)
print(x)