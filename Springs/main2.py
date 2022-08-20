import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from math import *
import os
import Animation_pygame

# import Animation

run_num = 1


def read_params(file_name):
    with open(file_name, "r") as file:
        data = json.load(file)
    file.close()

    dt = data['dt']
    l_rest = data['l_rest']
    k = data['k']
    mass = data['mass']
    osc_num = data['osc_num']
    amplitude = data['amplitude']
    frames_num = data['frames_num']
    first_is_open = data['first_is_open']
    last_is_open = data['last_is_open']
    err = data['err']
    return dt, l_rest, k, mass, osc_num, amplitude, frames_num, amplitude, first_is_open, last_is_open, err
    '''
    with open(file_name, "r") as file:
        for line in file: 
            line = line.split(" = ")
            if line[0]=='dt': 
                line = line[1].split(" ")
                dt_s = [float(dt) for dt in line[:-1]]
            elif line[0]=='l_rest': l_rest = float(line[1][:-1])
            elif line[0]=='k': k = float(line[1][:-1])
            elif line[0]=='mass': mass = float(line[1][:-1])
            elif line[0]=='osc_num': osc_num = int(line[1][:-1])
            #elif line[0]=='frames_num': frameses_num = int(line[1][:-1])
            elif line[0]=='frames_num': 
                line = line[1].split(" ")
                frameses_num = [int(frames_num) for frames_num in line[:-1]]
            elif line[0]=='amplitude': amplitude = float(line[1][:-1])
            elif line[0]=='err': err = float(line[1][:-1])
            
            elif line[0]=='first_is_open': 
                if (line[1][:-1] == 'False') or (line[1][:-1] == ''):
                    first_is_open = False
                else: 
                    first_is_open = True
            elif line[0]=='last_is_open':
                if (line[1][:-1] == 'False') or (line[1][:-1] == ''):
                    last_is_open = False
                else: 
                    last_is_open = True

    return dt_s, l_rest, k, mass, osc_num, amplitude, frameses_num, amplitude, first_is_open, last_is_open, err
    '''


dt_s, l_rest, k, mass, osc_num, amplitude, frameses_num, amplitude, first_is_open, last_is_open, err = read_params(
    "input_parameters" + str(run_num) + ".json")


def read_init_state(file_name):
    with open(file_name, "r") as f:
        data = json.load(f)
        x_s = data['x_s']
        v_s = data['v_s']

    return x_s, v_s
    '''
    x_s = []
    v_s = []
    with open(file_name, "r") as file:
        for line in file:
            line = line.split("\t")
            if line[0] == 'x_init':
                line.remove("x_init")
                #line.remove("\n")
                for x in line:
                    x_s.append(float(x))
            elif line[0] == 'v_init':
                line.remove("v_init")
                #line.remove("")
                for v in line:
                    v_s.append(float(v))
    return x_s, v_s
    '''


def move(x, v, a, dt):
    dv = a * dt
    v += dv
    dx = v * dt
    x += dx
    return x, v


def initial_grid():
    x_s = [0] * osc_num
    for i in range(osc_num):
        x_s[i] = x_s[0] + l_rest * i
    return x_s


def initial_grid2():
    x_s = [0] * osc_num
    for i in range(osc_num):
        x_s[i] = x_s[0] + l_rest * i

    v_s = [0] * osc_num
    a_s = [0] * osc_num
    f_s = [0] * osc_num
    return x_s, v_s, a_s, f_s


def initial_conditions(x_s, v_s):
    for i in range(1, osc_num - 1):
        if i % 2 == 0:
            x_s[i] += amplitude
        else:
            x_s[i] -= amplitude


def mean_frequency(x, t, dt):
    T = np.array([])
    t_s = np.array([])

    # only if the array is not constant. That is - the mass doesn't move at all.
    if not np.all(x == x[0]):
        indices, x_peaks = find_peaks(x, height=x[0])
        for i in indices:
            t_s = np.append(t_s, t[i])
        for i in range(len(indices) - 1):
            T = np.append(T, t_s[i + 1] - t_s[i])

        with open("outputs.txt", "a") as file:
            try:
                if T.mean() != 0:
                    frequency = 2 * np.pi / T.mean()
                    ex_frequency = sqrt(2 * k / mass)
                    file.write("{}\t{}\t{}".format(frequency, ex_frequency, abs(frequency - ex_frequency)))
                    file.write("\n")
                    with open("Ts.txt", "a") as file:
                        file.write("{}\t{}\t{}".format(T, dt, T.mean()))
                        file.write("\n")

            except:
                print("T is empty for dt=", dt)


def calc_wave_vel(v_t, time):
    if osc_num > 20:
        v = 0
        i = 0
        while v == 0:
            if v_t[i] != 0:
                v = osc_num / l_rest * time[i]
                break
            i += 1

    else:
        v = None

    return v


def Calc_E_tot(dx_s_t, v_s_t):
    E_k = 0.5 * mass * np.sum(v_s_t ** 2, axis=0)
    E_p = 0.5 * k * np.sum(dx_s_t ** 2, axis=0)
    E_tot = E_k + E_p
    return E_tot, E_k, E_p


def plot_E_t(E_t, E_k, E_p, t, dt):
    fig, ax = plt.subplots()
    ax.plot(t, E_t - E_t[0], label= "E total")
    #ax.plot(t, E_k , label= "E kinetik")
    #ax.plot(t, E_p, label= "E potential")
    ax.set(xlabel='t', ylabel='E(t) - E_0', title='E(t) - E_0 as function of time')
    ax.grid()
    ax.legend()
    fig.savefig("E_t_dt=" + str(dt) + ".png")


def plot_freq_vs_dt():
    diff = np.zeros(len(dt_s))
    i = 0
    with open("outputs.txt", "r") as file:
        for line in file:
            line = line.split("\t")
            # print(line)
            if not line[-1] == "nan":
                diff[i] = float(line[-1])
                i += 1

            '''
            if line[0]=="diff":
                diff[i] = float(line[1])
                i += 1
            '''
    fig, ax = plt.subplots()
    ax.plot(dt_s, diff)
    ax.set(xlabel='dt_s', ylabel='diff', title='frequencies diff vs dts')
    ax.grid()
    fig.savefig("f_vs_dt.png")


def main():
    # Before we begin delete the previous output file, if exist.
    try:
        os.remove("outputs.txt")
    except:
        pass

    for dt, frames_num in zip(dt_s, frameses_num):
        # Set al oscillators at resting positions. x_s_0 are the stability points of all the particles
        x_s_0 = np.array(initial_grid())

        # Set accelerations array
        a_s = np.zeros(osc_num)

        # Set forces array
        f_s = np.zeros(osc_num)

        # Set time array
        time = np.array([n * dt for n in range(frames_num)])

        # initial conditions
        x_s, v_s = read_init_state("input_initState" + str(run_num) + ".json")
        x_s = np.array(x_s)
        v_s = np.array(v_s)

        # frames_osc100_fra12000 will be a list of all the frames_osc100_fra12000, 
        # where each frame is a list of all particles poistions in each given time/frame
        frames = np.zeros([frames_num, osc_num])
        frames[0] = np.copy([x_s_0])

        # v_s_t, a_s_t will be metrices of the velocities and accelerations of each particle respectivly, orderd in time.
        # each row is an oscillator v(t) or a(t)
        v_s_t = np.zeros([frames_num, osc_num])
        v_s_t[0] = np.copy([v_s])
        a_s_t = np.zeros([frames_num, osc_num])

        # dx_s_t will a matrix of all dxs as function of time,
        # where dx is the displacement coordinate of each particle relative to it's stability point.
        dx_s_t = np.zeros([frames_num, osc_num])

        for frame_i in range(frames_num):
            dx_s = x_s - x_s_0
            dx_s_t[frame_i] = dx_s

            # first one
            if first_is_open:
                f_s[0] = -k * (dx_s[0] - dx_s[1])
                a_s[0] = f_s[0] / mass

            # All oscillators in between
            for i in range(1, osc_num - 1):
                f_s[i] += -k * (dx_s[i] - dx_s[i + 1]) - k * (dx_s[i] - dx_s[i - 1])
                a_s[i] = f_s[i] / mass

            # last one
            if last_is_open:
                f_s[osc_num - 1] += -k * (dx_s[osc_num - 1] - dx_s[osc_num - 2])
                a_s[osc_num - 1] = f_s[osc_num - 1] / mass

            # make all forces zero again before next frame
            f_s = np.zeros(osc_num)

            # final 2d array of all of the accelerations. Currently its all accelerations at a given time/frame
            a_s_t[frame_i] = a_s
            
            if frame_i == 0:
                v_s = v_s + a_s*0.5*dt
            else:                
                v_s = v_s + a_s*dt
                v_s_t[frame_i-1] = v_s - a_s_t[frame_i-1]*0.5*dt
            
            #x_s = x_s + v_s * dt + 0.5 * a_s * dt**2
            x_s = x_s + v_s * dt
            frames[frame_i] = x_s


        # From here on are calculations of the mean T time and mean frequency of each oscillator
        x_s_t = frames.T
        v_s_t = v_s_t.T
        a_s_t = a_s_t.T
        dx_s_t = dx_s_t.T
        E_tot, E_k, E_p = Calc_E_tot(dx_s_t, v_s_t)

        with open("Et.txt", "a") as file:
            for Et, Ek, Ep in zip(E_tot, E_k, E_p):
                file.write("{}\t{}\t{}".format(Et, Ek, Ep))
                file.write("\n")

        with open("x_t.txt", "w") as file:
            for x_s in x_s_t:
                for x in x_s:
                    file.write(str(x) + '\t')
                file.write('\n')

        with open("dx_t.txt", "w") as file:
            for dx in dx_s_t[1]:
                file.write(str(dx) + '\t')
            file.write('\n')

        with open("v_t.txt", "w") as file:
            for v in v_s_t[1]:
                file.write(str(v) + '\t')
            file.write('\n')

        with open("a_t.txt", "w") as file:
            for a_s in a_s_t:
                for a in a_s:
                    file.write(str(a) + '\t')
                file.write('\n')

                # Calculate the mean frequency of the middle oscillator
        mean_frequency(x_s_t[int(osc_num / 2)], time, dt)

        # Calculate the velocitie of wave in case of frames_num>20
        v_wave = calc_wave_vel(v_s_t[osc_num - 1, :], time)
        # print("Wave velocity numerically: ", v_wave)
        # print("Wave velocity analiticly: ", sqrt(k/mass)*l_rest)

        # Writing to files parameters
        file_num = 0
        file_dir = "frames_osc100_fra12000"

        # Remove frames_osc100_fra12000 files of previous run
        for i in range(100001):
            try:
                os.remove(file_dir + "/" + "frame" + str(i) + ".txt")
            except:
                pass
        os.rmdir(file_dir)
        # recreate the directory of all frames_osc100_fra12000
        os.mkdir(file_dir)

        if dt > 0.07:
            fig, ax = plt.subplots()
            for i in range(int(osc_num / 2), int(osc_num / 2) + 1):
                # ax.plot(time, x_s_t[i], label='x(t)')
                ax.plot(time, a_s_t[i], label='a(t)')
                ax.plot(time, v_s_t[i], label='v(t)')
                ax.plot(time, dx_s_t[i], label='dx(t)')
            ax.set(xlabel='time', ylabel='a, v, dx', title='oscillators')
            ax.legend()
            ax.grid()
            fig.savefig("x_t" + str(dt) + ".png")
            plt.close()

        for frame in frames:
            # write frame file
            with open(file_dir + "/" + "frame" + str(file_num) + ".txt", "w") as file:
                for x in frame:

                    file.write(str(x) + '\t')
            file_num += 1

        # if dt<0.2:
        #Animation_pygame.play(osc_num, int(frames_num/2), dt)
        file.close()

        plot_E_t(E_tot, E_k, E_p, time, dt)

    plot_freq_vs_dt()


if __name__ == '__main__':
    main()

