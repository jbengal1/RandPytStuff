import matplotlib.pyplot as plt
import numpy as np
import os

N = 100
dir_name = "build_frames"
animation_file_name = 'animation'
OPEN_ANIM = True

def f1(x, i):
    return np.sin(x + i/16)*np.exp(-x*i/4000)

def f2(x, i):
    return np.sin(-x - i/16)*np.exp(x*i/4000)

x = np.linspace(0, 2*np.pi, 100)

for i in range(N):
    y1 = f1(x, i)
    y2 = f2(x, i)
    plt.plot(x, y1, color='k')
    plt.plot(x, y2, color='b')
    plt.ylim(-2, 2)
    plt.title(f"frame{i}")
    plt.savefig(f'{dir_name}/' + 'frame'+str(i).zfill(3)+'.png')
    plt.close()

os.chdir(dir_name)
stream = os.popen('convert -delay 4 frame* {animation_file_name}.gif')

if OPEN_ANIM:
    os.popen('xdg-open {animation_file_name}.gif')