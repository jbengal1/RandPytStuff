import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from math import *
import os, sys
import time as TIME

# Measure current real time
start_time = TIME.time()

if len(sys.argv)>1:
    file_num = sys.argv[1]
else:
    file_num = 3




def read_params(file_name):
    with open(file_name, "r") as file:
        data = json.load(file)
    file.close()

    frames_nums = data['frames_num']
    dts = data['dt']
    l_rest = data['l_rest']
    k = data['k']
    mass = data['mass']
    omega = data['omega']
    osc_num = data['osc_num']
    first_is_open = data['first_is_open']
    last_is_open = data['last_is_open']
    return frames_nums, dts, l_rest, k, mass, omega, osc_num, first_is_open, last_is_open


# If these lines exist, the parameters will be according to the files.
file_name = "input_parameters" + str(file_num) + ".json"
frames_nums, dts, l_rest, k, mass, omega, osc_num, first_is_open, last_is_open = read_params(file_name)
if omega:
    T_period = 2*pi/omega


def write_to_files(data, file_dir):
    file_num = 0
    if not os.path.isdir(file_dir):
        os.mkdir("frames")
    for line in data:
        # write frame file
        with open(f"{file_dir}/frame{file_num}.txt", "w") as file:
            for x in line:
                # file.write(f"{x}\n")
                file.write(f"{x}\t")

        file_num += 1


def write_to_file(data, file_name):
    """ writes any data into a single file """
    for line in data:
        with open(f"{file_name}.txt", "a") as file:
            for x in line:
                file.write(f"{x}\t")
            file.write("\n")


def delete_prev_files(file_dir):
    done = False
    i = 0
    while not done:
        file = f"{file_dir}/frame{i}.txt"
        if os.path.isfile(file):
            os.remove(file)
            i += 1
        else:
            done = True


def plot_graphs(dic1, dic2, file_name, type_graph, time):
    if omega is not None:
        x_analytic = np.cos(omega*time)
        v_analytic = -omega*np.sin(omega*time)
        a_analytic = -(omega**2)*np.cos(omega*time)

    fig, ax = plt.subplots()
    # If this simulation is one oscillator between two walls
    if osc_num == 3:
        if type_graph == 'x':
            ax.plot(time, x_analytic, label='Analytic x')
            ax.plot(time, v_analytic, label='Analytic v')
            ax.plot(time, a_analytic, label='Analytic a')
        for key, value in dic1.items():
            ax.plot(time, value, label=key)
    # If this simulation is two oscillator between two walls
    elif osc_num == 4:
        for key, value in dic1.items():
            ax.plot(time, value, label=key)
        for key, value in dic2.items():
            ax.plot(time, value, label=key)
    else:
        for key, value in dic1.items():
            ax.plot(time, value, label=key)
    ax.legend()
    ax.grid()
    fig.savefig(file_name + ".png")
    plt.close()


def initial_conditions(file_name):
    with open(file_name, "r") as file:
        data = json.load(file)
    file.close()
    return data["x"], data["v"]


def calculate_force(dx):
    f = np.zeros(osc_num)
    for i in range(osc_num):
        if i == 0:
            if first_is_open:
                f[i] = -k*(dx[i] - dx[i+1])
        elif i == osc_num - 1:
            if last_is_open:
                f[i] = -k*(dx[i] - dx[i-1])
        else:
            f[i] = -k*(2*dx[i] - dx[i-1] - dx[i+1])
    return f


def Calc_E_tot(dx_t, v_t):
    E_k = 0.5 * mass * np.sum(v_t ** 2, axis=0)
    E_p = 0
    for i in range(len(dx_t) - 1):
        E_p += 0.5 * k *(dx_t[i+1] - dx_t[i])**2
    E_tot = E_k + E_p
    return E_tot, E_k, E_p


def mean_frequency(dx, t, dt):
    if (osc_num == 3) or (osc_num == 4):
        T = np.array([])
        t_peaks = np.array([])

        # only if the array is not constant. That is - the mass doesn't move at all.
        if not np.all(dx == dx[0]):
            indices, x_peaks = find_peaks(dx, height=0)
            for i in indices:
                t_peaks = np.append(t_peaks, t[i])
            for i in range(len(indices) - 1):
                T = np.append(T, t_peaks[i + 1] - t_peaks[i])

            with open("frequencies.txt", "a") as file:
                try:
                    if T.mean() != 0:
                        frequency = 2 * np.pi / T.mean()
                        ex_frequency = omega
                        file.write("{}\t{}\t{}".format(frequency, ex_frequency, abs(frequency - ex_frequency)))
                        file.write("\n")
                        with open("Ts.txt", "a") as file:
                            file.write("{}\t{}\t{}".format(T, dt, T.mean()))
                            file.write("\n")

                except:
                    print("T is empty for dt=", dt)


def plot_freq_vs_dt():
    if len(dts) > 1:
        diff = np.zeros(len(dts))
        i = 0
        with open("frequencies.txt", "r") as file:
            for line in file:
                line = line.split("\t")
                if not line[-1] == "nan" and line[0] != "num_frequency":
                    diff[i] = float(line[-1])
                    i += 1

        fig, ax = plt.subplots()
        ax.plot(dts, diff)
        ax.set(xlabel='dts', ylabel='diff', title='frequencies diff vs dts')
        ax.grid()
        fig.savefig("freq_vs_dt.png")
    else:
        pass


def calc_wave_v(v_t, time):
    for i, v in enumerate(v_t[:, -1]):
        if v != 0:
            print("first movement of the last oscillator at (index, time, velocity):", i, time[i], v)
            print("Time passed to last osc moving:", time[i])
            return (l_rest*(osc_num-1))/time[i]

# Set all kinematics variables
x_0 = np.array([n*l_rest for n in range(osc_num)])
v_0 = np.zeros(osc_num)


def leap_frog(dt, frames_num):
    print("dt, frames_num, osc_num = ", dt, frames_num, osc_num)
    time = np.linspace(0, dt * frames_num, frames_num)
    x, v = initial_conditions("input_initState" + str(file_num) + ".json")
    dx = x - x_0
    x_t = np.copy([x])
    dx_t = np.copy([dx])
    v_t = np.copy([v])

    f = calculate_force(dx)
    a = f / mass
    a_t = np.copy([a])

    for frame_i in range(1, frames_num + 1):
        if frame_i == 1:
            v = v + a * dt / 2
        else:
            v = v + a * dt
            # v_whole = v - dt*(a_old + a)/2
            v_whole = v - dt * a / 2
            v_t = np.append(v_t, [v_whole], axis=0)

        x = x + v * dt
        dx = x - x_0

        f = calculate_force(dx)
        a = f / mass

        x_t = np.append(x_t, [x], axis=0)
        dx_t = np.append(dx_t, [dx], axis=0)
        a_t = np.append(a_t, [a], axis=0)
        # print what number of frame every 1000 frames_osc100_fra12000
        if frame_i%1000 == 0:
            print(f"Finished working on frame {frame_i}")

    # Delete last element, as the velocity array will always have one last whole step missing.
    x_t = np.delete(x_t, -1, 0)
    dx_t = np.delete(dx_t, -1, 0)
    a_t = np.delete(a_t, -1, 0)
    # print(dx_t.T[-1][:20])
    # print(v_t.T[-1][:20])
    # print(a_t.T[-1][:20])
    return time, x_t, dx_t, v_t, a_t


def main():
    for dt, frames_num in zip(dts, frames_nums):

        time, x_t, dx_t, v_t, a_t = leap_frog(dt, frames_num)

        # Before we write to file, delete the previous output file,and rewrite the titles
        with open("outputs.txt", "w") as file:
            file.write(
                "{}\t{}\t{}".format("num_frequency", "analytic_frequency", "|num_frequency - analytic_frequency|"))
            file.write("\n")

        delete_prev_files("frames")
        # write_to_files(x_t, "frames")
        write_to_file(x_t, "frames")

        dic1 = {
            "numeric x1": dx_t.T[int(osc_num / 2)],
            "numeric v1": v_t.T[int(osc_num / 2)],
            "numeric a1": a_t.T[int(osc_num / 2)]
            }
        dic2 = {
            "numeric x2": dx_t.T[int(osc_num / 2 - 1)],
            "numeric v2": v_t.T[int(osc_num / 2 - 1)],
            "numeric a2": a_t.T[int(osc_num / 2 - 1)]
        }

        plot_graphs(dic1, dic2, f"x_t{frames_num}", "x", time)

        E_tot, E_k, E_p = Calc_E_tot(dx_t.T, v_t.T)

        dic_Energies = {
            "E total": E_tot,
            "Energy kinetic": E_k,
            "Energy potential": E_p
            }
        plot_graphs(dic_Energies, {}, f"E_{frames_num}", "", time)

        # Calculate the mean frequencies and write it to "frequencies.txt"
        mean_frequency(dx_t.T[int(osc_num / 2)], time, dt)

        finish_time = TIME.time()
        print(f"Run time is: {round(finish_time - start_time, 2)} seconds")

        if osc_num > 30:
            v_wave = calc_wave_v(v_t, time)
            v_an = sqrt(k/mass)*l_rest
            print("for osc_num = ", osc_num)
            print(v_wave, v_an)
            try:
                rel_err = abs(v_wave - v_an)/v_an
                print("relative error:", rel_err*100, "%")
                file_name = "v_wave"
                write_to_file([[v_an, v_wave, rel_err]], file_name)
            except NameError:
                print(NameError)
    # plot frequency vs dt
    plot_freq_vs_dt()


    # Animation.play()

if __name__ == "__main__":
    main()


