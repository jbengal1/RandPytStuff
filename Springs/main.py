import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from math import *
import os
import Animation_pygame

# import Animation

run_num = 1


def read_params(file_name):
    with open(file_name, "r") as file:
        for line in file:
            line = line.split(" = ")
            if line[0] == 'dt':
                line = line[1].split(" ")
                dt_s = [float(dt) for dt in line[:-1]]
            elif line[0] == 'l_rest':
                l_rest = float(line[1][:-1])
            elif line[0] == 'k':
                k = float(line[1][:-1])
            elif line[0] == 'mass':
                mass = float(line[1][:-1])
            elif line[0] == 'osc_num':
                osc_num = int(line[1][:-1])
            # elif line[0]=='frames_num': frameses_num = int(line[1][:-1])
            elif line[0] == 'frames_num':
                line = line[1].split(" ")
                frameses_num = [int(frames_num) for frames_num in line[:-1]]
            elif line[0] == 'amplitude':
                amplitude = float(line[1][:-1])
            elif line[0] == 'err':
                err = float(line[1][:-1])

            elif line[0] == 'first_is_open':
                if (line[1][:-1] == 'False') or (line[1][:-1] == ''):
                    first_is_open = False
                else:
                    first_is_open = True
            elif line[0] == 'last_is_open':
                if (line[1][:-1] == 'False') or (line[1][:-1] == ''):
                    last_is_open = False
                else:
                    last_is_open = True

    return dt_s, l_rest, k, mass, osc_num, amplitude, frameses_num, amplitude, first_is_open, last_is_open, err


#dt_s, l_rest, k, mass, osc_num, amplitude, frameses_num, amplitude, first_is_open, last_is_open, err = read_params("input_parameters" + str(run_num) + ".txt")
dt_s, l_rest, k, mass, osc_num, amplitude, frameses_num, amplitude, first_is_open, last_is_open, err = [0.1], 10, 4, 1, 3, 1, [100], 1, 0.1, False, False

# print(dt, l_rest, k, mass, osc_num, amplitude, frames_num, amplitude, first_is_open, last_is_open, err)


def read_init_state(file_name):
    x_s = []
    v_s = []
    with open(file_name, "r") as file:
        for line in file:
            line = line.split("\t")
            if line[0] == 'x_init':
                line.remove("x_init")
                # line.remove("\n")
                for x in line:
                    x_s.append(float(x))
            elif line[0] == 'v_init':
                line.remove("v_init")
                # line.remove("")
                for v in line:
                    v_s.append(float(v))
    return x_s, v_s


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


def restart_forces(f_s):
    for i in range(osc_num):
        f_s[i] = 0


def mean_frequency(x, t):
    T = np.array([])
    t_s = np.array([])

    # only if the array is not constant. That is - the mass doesn't move at all.
    if not np.all(x == x[0]):
        with open("outputs.txt", "a") as file:
            indices, x_peaks = find_peaks(x, height=x[0])
            for i in indices:
                t_s = np.append(t_s, t[i])
            for i in range(len(indices) - 1):
                T = np.append(T, t_s[i + 1] - t_s[i])

            if T.mean() != 0:
                frequency = 2 * np.pi / T.mean()
                file.write("Numerical frequency: " + str(frequency) + "\n")
                ex_frequency = sqrt(2 * k / mass)
                file.write("Exact frequency: " + str(ex_frequency) + "\n")
                file.write("diff : " + str(frequency - ex_frequency) + "\n")


def calc_wave_vel(v_t, time):
    if osc_num > 20:
        v = 0
        i = 0
        while v == 0:
            if v_t[i] != 0:
                print(i, time[i])
                v = osc_num / l_rest * time[i]
                break
            i += 1

    else:
        v = None

    return v


def Calc_E_tot(x_s, v_s):
    E_tot = 0
    for v in v_s:
        E_tot += 0.5 * mass * v ** 2
    for i in range(len(x_s) - 1):
        E_tot += 0.5 * k * (x_s[i + 1] - x_s[i]) ** 2
    return np.mean(E_tot)


def plot_freq_vs_dt():
    diff = np.zeros(len(dt_s))
    i = 0
    with open("outputs.txt", "r") as file:
        for line in file:
            line = line.split(" : ")
            print(line)
            if line[0] == "diff":
                diff[i] = float(line[1])
                i += 1

    print(diff)
    fig, ax = plt.subplots()
    ax.scatter(dt_s, diff)
    ax.set(xlabel='dt_s', ylabel='diff', title='frequencies diff vs dts')
    ax.grid()
    fig.savefig("f_vs_dt.png")


def main():
    for dt, frames_num in zip(dt_s, frameses_num):
        x_s = initial_grid()
        a_s = [0] * osc_num
        f_s = [0] * osc_num

        # An array to "record" time
        time = np.array([0])

        # x_s_0 are the stability points of all the particles
        x_s_0 = x_s.copy()

        # frames_osc100_fra12000 will be a list of all the frames_osc100_fra12000, 
        # where each frame is a list of all particles poistions in each given time/frame
        frames = np.array([x_s])

        # initial conditions
        x_s, v_s = read_init_state("input_initState" + str(run_num) + ".txt")

        # v_s_t, a_s_t will be the velocities and accelerations of each particle respectivly, orderd in time. 
        v_s_t = np.array([v_s])
        a_s_t = np.array([a_s])

        for frame_i in range(frames_num):

            # first one
            if first_is_open:
                # the dx's are displacment coordinate of each particle relative to it's stability point.
                dx1 = x_s[0] - x_s_0[0]
                dx2 = x_s[1] - x_s_0[1]
                f_s[0] = -k * (dx1 - dx2)
                a_s[0] = f_s[0] / mass

            # All between
            for i in range(1, osc_num - 1):
                dx1 = x_s[i] - x_s_0[i]
                dx2 = x_s[i + 1] - x_s_0[i + 1]
                f_s[i] += -k * (dx1 - dx2)

                dx1 = x_s[i] - x_s_0[i]
                dx2 = x_s[i - 1] - x_s_0[i - 1]
                f_s[i] += -k * (dx1 - dx2)

                a_s[i] = f_s[i] / mass

            # last one
            if last_is_open:
                dx1 = x_s[osc_num - 1] - x_s_0[osc_num - 1]
                dx2 = x_s[osc_num - 2] - x_s_0[osc_num - 2]
                f_s[osc_num - 1] += -k * (dx1 - dx2)
                a_s[osc_num - 1] = f_s[osc_num - 1] / mass

            # After all accelerations have been calculated, now we move all the oscillators
            for i in range(osc_num):
                x_s[i], v_s[i] = move(x_s[i], v_s[i], a_s[i], dt)

            # make all forces zero again before next frame
            restart_forces(f_s)

            # finale 2d array of all of the frames_osc100_fra12000. Each row is an array of locations in a given frame.
            frames = np.append(frames, [x_s], axis=0)
            v_s_t = np.append(v_s_t, [v_s], axis=0)
            a_s_t = np.append(a_s_t, [a_s], axis=0)
            # we record the time passed, in order to calculate the T time and the frequency
            time = np.append(time, dt * frame_i)

        frames = np.delete(frames, 0, 0)
        time = np.delete(time, 0, 0)

        # From here on are calculations of the mean T time and mean frequency of each oscillator
        x_s_t = frames.T
        v_s_t = v_s_t.T
        a_s_t = a_s_t.T

        # Calculate the the total energy in time. That is, E(t).
        E_t = Calc_E_tot(x_s_t, v_s_t)
        print(E_t)

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
        for i in range(int(osc_num / 2 - 1), int(osc_num / 2 - 1) + 2):
            ax.plot(time, x_s_t[i])
        ax.set(xlabel='time', ylabel='x', title='oscilators')
        ax.grid()
        fig.savefig("test" + str(dt) + ".png")

        # Calculate the mean frequency of the middle oscillator
        mean_frequency(x_s_t[int(osc_num / 2)], time)

        # Calculate the velocitie of wave in case of frames_num>20
        v_wave = calc_wave_vel(v_s_t[osc_num - 1, :], time)
        # print("Wave velocity numerically: ", v_wave)
        # print("Wave velocity analiticly: ", sqrt(k/mass)*l_rest)

        # Writing to files parameters
        file_num = 0
        file_dir = "frames_osc100_fra12000"

        # Remove frames_osc100_fra12000 files of previous run
        for i in range(50001):
            try:
                os.remove(file_dir + "/" + "frame" + str(i) + ".txt")
            except:
                pass
        os.rmdir(file_dir)
        # recreate the directory of all frames_osc100_fra12000
        os.mkdir(file_dir)

        for frame in frames:
            # write frame file
            with open(file_dir + "/" + "frame" + str(file_num) + ".txt", "w") as file:
                for x in frame:
                    file.write(str(x) + '\t')
            file_num += 1

        # Animation_pygame.play(osc_num, frames_num, dt)
        file.close()

    plot_freq_vs_dt()


if __name__ == '__main__':
    main()
