import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from math import *
import os
import Animation_pygame
#import Animation


frames_num = 10
osc_num = 2
dt = 0.1
k = 4
l_rest = 10
mass = 1

first_is_open = True
last_is_open = True

amplitude = 0.1*l_rest
err = 0.1


def move(x, v, a):
    dv = a*dt
    v += dv
    dx = v*dt
    x += dx
    return x, v


def apply_force(force):
    a = force/mass
    return a


def spring_force(dx1, dx2):
    return k*(dx1 - dx2)


def initial_grid(x_s, v_s, a_s, f_s):
    for i in range(1, osc_num):
        x_s = np.append(x_s, x_s[0] + np.array([1, 0])*l_rest*i)
        v_s = np.append(v_s, [0, 0])
        a_s = np.append(a_s, [0, 0])
        f_s = np.append(f_s, [0, 0])


def initial_conditions(x_s, v_s):
    direction = np.array([1, 0])
    for i in range(1, osc_num-1):
        if i%2==0:
            x_s[i] += amplitude*direction
        else:    
            x_s[i] -= amplitude*direction


def restart_forces(f_s):
    size = len(f_s)
    f_s = np.zero((size, size))

'''
def compare_frames(frame1, frame2):
    flag = True
    i = 0 
    while flag:        
        if np.abs(frame1[i] - frame2[i]) > err:
            flag = False
            break
        i += 1
        if i==osc_num-1:
            break
        
    
    return flag
'''

def mean_frequency(x, t, err): 
    T = np.array([])
    t_s = np.array([])
    
    # only if the array is not constant. That is - the mass doesn't move at all.
    if not np.all(x == x[0]):
        with open("outputs.txt", "w") as file:   
            indices, x_peaks = find_peaks(x, height=x[0])
            for i in indices:
                t_s = np.append(t_s, t[i])
            for i in range(len(indices)-1):
                T = np.append(T, t_s[i+1] - t_s[i])

            if T.mean()!=0:
                frequency = 2*np.pi/T.mean()
                file.write("Numerical frequency: " + str(frequency) + "\n")
                ex_frequency = sqrt(k/mass)
                file.write("Exact frequency: " + str(ex_frequency) + "\n")
                file.write("diff : " + str(frequency - ex_frequency) + "\n")


def main():
    
    x_s = [0,0]
    v_s = np.array([[0,0]])
    a_s = np.array([[0,0]])
    f_s = np.array([[0,0]])
    
    # An array to "record" time
    time = np.array([0])
    print(x_s)
    initial_grid(x_s, v_s, a_s, f_s)
    print(x_s)
    # Another method to initialize all kinemtics
    #x_s, v_s, a_s, f_s = initial_grid2()
    
    x_s_0 = x_s.copy()
    v_s_t = np.array([v_s])
    a_s_t = np.array([a_s])
    frames = np.array([x_s])

    # initial conditions
    initial_conditions(x_s, v_s)

    
    for frame_i in range(frames_num):
        
        # first one
        if first_is_open:
            dx2 = x_s[0] - x_s_0[0]
            dx1 = x_s[1] - x_s_0[1]
            f_s[0] = spring_force(dx1, dx2)
            a_s[0] = apply_force(f_s[0])

        # All between
        for i in range(1, osc_num-1):
            dx1 = x_s[i+1] - x_s_0[i+1]
            dx2 = x_s[i] - x_s_0[i]
            f_s[i] += spring_force(dx1, dx2)

            dx1 = x_s[i-1] - x_s_0[i-1]
            dx2 = x_s[i] - x_s_0[i]
            f_s[i] += spring_force(dx1, dx2)

            a_s[i] = apply_force(f_s[i])

        # last one
        if last_is_open:
            dx1 = x_s[osc_num - 2] - x_s_0[osc_num - 2]
            dx2 = x_s[osc_num - 1] - x_s_0[osc_num - 1]
            f_s[osc_num - 1] += spring_force(dx1, dx2)
            a_s[osc_num - 1] = apply_force(f_s[osc_num - 1])

        # After all accelerations have been calculated, now we move all the oscillators
        for i in range(osc_num):
            x_s[i], v_s[i] = move(x_s[i], v_s[i], a_s[i])

        # make all forces zero again before next frame
        restart_forces(f_s)

        # finale 2d array of all of the frames. Each row is an array of locations in a given frame.
        frames = np.append(frames, [x_s], axis=0)
        v_s_t =  np.append(v_s_t, [v_s], axis=0)
        a_s_t =  np.append(a_s_t, [a_s], axis=0)
        # we record the time passed, in order to calculate the T time and the frequency
        time = np.append(time, dt*frame_i)


    # From here on are calculations of the mean T time and mean frequency of each oscillator
    x_s_t = frames.T
    v_s_t = v_s_t.T
    a_s_t = a_s_t.T

    with open("x_t.txt", "w") as file:
        for x_s in x_s_t:
            for x in x_s:
                file.write(str(x) + '\t')
            file.write('\n')

    with open("v_t.txt", "w") as file:
        for v_s in v_s_t:
            for v in v_s:
                file.write(str(v) + '\t')
            file.write('\n')

    with open("a_t.txt", "w") as file:
        for a_s in a_s_t:
            for a in a_s:
                file.write(str(a) + '\t')
            file.write('\n') 
    
    fig, ax = plt.subplots()
    for i in range(int(osc_num/2 -1), int(osc_num/2 -1) + 2):
        ax.plot(time, x_s_t[i])
    ax.set(xlabel='time', ylabel='x', title='oscilators')
    ax.grid()
    fig.savefig("test.png")
    
    # Calculate the mean frequency of the middle oscillator
    mean_frequency(x_s_t[int(osc_num/2)], time, err)
    
    file_num = 0
    file_dir = "frames"
    

    # Remove frames files of previous run
    for i in range(100001):
        try:
            os.remove(file_dir+"/" + "frame" + str(i) + ".txt")
        except:
            pass
    os.rmdir(file_dir)
    # recreate the directory of all frames
    os.mkdir(file_dir)


    for frame in frames:
        # write frame file
        with open(file_dir+"/" + "frame" + str(file_num) + ".txt", "w") as file:
            for x in frame:
                file.write(str(x) + '\t')
        file_num += 1

    Animation_pygame.play(osc_num, frames_num)
    file.close()


if __name__ == '__main__':
    main()
