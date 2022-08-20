import numpy as np
import json
import matplotlib.pyplot as plt
from scipy import signal

from math import sqrt
import os, sys

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# You can run the code as is (default number is 3),
# or run it with an argument (int) to pick the input files pair,
# or change the default number (the variable FILE_NUM bellow) and then run.
# 
# The code's structure:
# 1. Set global parameters
# 2. Define all functions
# 3. Call the function main(), which calls each of the other functions
# 
# All the functions used from os and sys modules are optional.
# The code can be just fine without them.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#  1. Set Global Parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define number of input by given input, if given. Else default is 3.
# Assuming the names are "input_parametersi.json" "input_initStatei.json"
if len(sys.argv) > 1:
    FILE_NUM = sys.argv[1]
else:
    FILE_NUM = 3

# Set input parameter file name
param_file_name = f"input_parameters{FILE_NUM}.json"
initState_file_name = f"input_initState{FILE_NUM}.json"

# Check if the inputs files exist (totally optional)
if os.path.isfile(param_file_name) and os.path.isfile(initState_file_name):
    # Load data from input parameter file
    with open(param_file_name, "r") as param_file:
        data = json.load(param_file)
    param_file.close()

    # Get global parameters
    FRAMES_NUMs = data['frames_num']
    DTs = data['dt']
    L_REST = data['l_rest']
    K = data['k']
    MASS = data['mass']
    OMEGA = data['omega']
    OSC_NUM = data['osc_num']
    FIRST_IS_OPEN = data['first_is_open']
    LAST_IS_OPEN = data['last_is_open']

    # If the input files are found we can run everything.
    RUN = True

else:
    print("No input file", param_file_name)
    RUN = False


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#  2. Define all functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

""" Read and returns the initial state (x(0), v(0)) from the input file """
def initial_conditions():
    with open(initState_file_name, "r") as file:
        init_dict = json.load(file)
    file.close()
    return init_dict["x"], init_dict["v"]


""" writes any array data into a single file """
def write_to_file(data_arr, file_name):
    file = open(f"{file_name}.txt", "w")
    for line in data_arr:
        for x in line:
            file.write(f"{x}\t")
        file.write("\n")

    file.close()


""" plots the given data, and save the plot in a png file """
def plot_graphs(data_dict, xAxis_data, xAxis_title, title, file_name):

    fig, ax = plt.subplots()
    for Key, value in data_dict.items():
        ax.plot(xAxis_data, value, label=Key)

    # Set title
    ax.set_title(title)

    # Set x axis title
    ax.set_xlabel(xAxis_title)

    # Set legend
    ax.legend()

    # Set grid
    ax.grid()

    # Save figure to file
    fig.savefig(file_name + ".png")
    plt.close() # (Necessary to tell python - don't keep plotting over the next figures)


""" calculate the forces of all oscillators in the chain in a given time/step """
def calc_force(dx):
    f = np.zeros(OSC_NUM)
    for n in range(OSC_NUM):
        if n == 0:
            if FIRST_IS_OPEN:
                f[n] = -K*(dx[n] - dx[n+1])
        elif n == OSC_NUM - 1:
            if LAST_IS_OPEN:
                f[n] = -K*(dx[n] - dx[n-1])
        else:
            f[n] = -K*(2*dx[n] - dx[n-1] - dx[n+1])
    return f


""" calculate and return the kinetic, potential and total energy of the chain """
def calc_E(dx, v):
    E_K = 0.5 * MASS * np.sum(v ** 2, axis=0)
    E_p = 0
    for i in range(len(dx) - 1):
        E_p += 0.5 * K *(dx[i+1] - dx[i])**2
    E_tot = E_K + E_p
    return E_tot, E_K, E_p


""" calculate and return the frequency of the middle oscillator by approximating it's time period """
def mean_frequency(dx, t, dt):
    # We want only these specific cases
    if (OSC_NUM <=4) and (not FIRST_IS_OPEN) and (not LAST_IS_OPEN):

        # And only if the array is not constant. That is - if the mass moves at all.
        if not np.all(dx == dx[0]):

            # Set empty arrays
            T = np.array([])
            t_peaks = np.array([])

            # get the indices of all local maximums
            indices, x_peaks = signal.find_peaks(dx, height=0)

            # Make sure there are maximums in dx(t). 
            if len(indices) != 0:
                t_peaks = t[indices]
                for i in range(len(indices) - 1):
                    T = np.append(T, t_peaks[i + 1] - t_peaks[i])
            # (The function find_peaks might not find in some cases. 
            # For example, when dx's motion will show only 1 or no time period)

            # Calculate the frequency by the avarage of all the Ts found
            if len(T) != 0:
                frequency = 2 * np.pi / T.mean()
            else:
                print("Error calculating T, for dt =", dt)
                frequency = None

            return frequency


""" 
Calculate approximated wave velocity 
due to a small disturbance at one end of a long oscillators chain.
v refers to the velocity of the last oscillator, and t is an array of all times.
"""
def calc_wave_v(v, t):
    for i, v in enumerate(v):
        if v != 0:
            return (L_REST*(OSC_NUM-1))/t[i]


""" 
Simulate the chain motion using the Leapfrog integration method, 
for a given time step dt and number of frames frames_num.
"""
def leap_frog(dt, frames_num):

    # Set arrays of initial state
    x, v = initial_conditions()

    # Set an array of rest potistions, and dx of all oscillators
    x_rest = np.array([n*L_REST for n in range(OSC_NUM)])
    dx = x - x_rest

    # Initialize data arrays, so we can save all infromation we need
    x_data = np.copy([x])
    dx_data = np.copy([dx])
    v_data = np.copy([v])

    # calculate the forces apllied on all oscillators at t=0
    f = calc_force(dx)

    # calculate the accelerations of all oscillators at t=0
    a = f / MASS
    a_data = np.copy([a])

    # We loop over all steps from 1 to frames_num+1 
    for frame_i in range(1, frames_num + 1):
    # (The reason for this is to have enough velocities. 
    # Later we delete x_data, dx_data and a_data last row.
    # Otherwise the velocities array will have one last whole step missing.)

        # calcualte the velocities of all oscillators at each time step
        if frame_i == 1:

            # first step advanced by dt/2
            v = v + a * dt / 2

        else:

            # All other steps by whole dt
            v = v + a * dt

            # time regression by dt/2 back, to get v at whole time steps.
            v_whole = v - dt * a / 2
            v_data = np.append(v_data, [v_whole], axis=0)

        # calcualte the x, dx of all oscillators at each time step
        x = x + v * dt
        dx = x - x_rest

        # calculate the forces apllied on all oscillators at each time step
        f = calc_force(dx)

        # calculate the accelerations of all oscillators at each time step
        a = f / MASS

        # Afte each step append the results to the data arrays
        x_data = np.append(x_data, [x], axis=0)
        dx_data = np.append(dx_data, [dx], axis=0)
        a_data = np.append(a_data, [a], axis=0)

        # print what number of frame is being computed every 1000 frames
        if frames_num > 3000 and frame_i%1000 == 0:
            print(f"Finished working on frame {frame_i}")

    # Delete last row at each
    x_data = np.delete(x_data, -1, axis=0)
    dx_data = np.delete(dx_data, -1, axis=0)
    a_data = np.delete(a_data, -1, axis=0)
    return x_data, dx_data, v_data, a_data


""" the main function, that organizes everything """
# The function's structure is relatively simple,
# but obviously there are many ways in which it can be constructed.
def main():

    # Set an empty array of the frequencies data 
    freq_data_arr = np.empty((0, 3))

    # Loop over all the dts and frames_nums parameters in the lists.
    for dt, frames_num in zip(DTs, FRAMES_NUMs):

        # It's nice to follow the progression while waiting
        print(f"dt = {dt}, frames_num = {frames_num}, OSC_NUM = {OSC_NUM}\n")

        # Set an array of all times
        time = np.linspace(0, dt * frames_num, frames_num)

        # Run a single leapfrog method simulation,
        # and get all the kinematics information we need.
        x_data, dx_data, v_data, a_data = leap_frog(dt, frames_num)

        # Calculate the approximated frequency
        dx_mid_osc = dx_data.T[int(OSC_NUM / 2)]
        freq_approx = mean_frequency(dx_mid_osc, time, dt)

        # Calculate the frequency relative error and write to file
        if freq_approx is not None:
            freq_error = abs(freq_approx - OMEGA)/OMEGA
        else:
            freq_error = None

        # Save all frequencies data into one array
        freq_data_arr = np.append(freq_data_arr, [[OMEGA, freq_approx, freq_error]], axis=0)

    # Get 3 arrays of the kinetic, potential and total energies in time.
    E_tot, E_K, E_p = calc_E(dx_data.T, v_data.T)

    # Write all coordinates to the frames.txt file
    write_to_file(x_data, "frames")

    # Write all frequencies and their errors to the frequencies.txt file
    write_to_file(freq_data_arr, file_name="frequencies")

    # plot kinematics
    kinematics_dict = {
        "a(t)": a_data.T[int(OSC_NUM / 2)],
        "v(t)": v_data.T[int(OSC_NUM / 2)],
        "dx(t)": dx_data.T[int(OSC_NUM / 2)]
        }
    plot_graphs(kinematics_dict, xAxis_data=time, xAxis_title="t", title="kinematics", file_name="kinematics")

    # plot energies
    Energies_dict = {
        "E_tot(t)": E_tot,
        "E_k(t)": E_K,
        "E_p(t)": E_p
        }
    plot_graphs(Energies_dict, xAxis_data=time, xAxis_title="t", title="Energies", file_name="Energy")

    # Calculate and write wave velocity for long enough chain
    if OSC_NUM > 100:
        v_wave_approx = calc_wave_v(v_data[:, -1], time)
        v_wave_theory = sqrt(K/MASS)*L_REST

        try:
            v_wave_err = abs(v_wave_approx - v_wave_theory)/v_wave_theory
        except NameError:
            v_wave_err = None
            print(NameError)

        write_to_file([[v_wave_theory, v_wave_approx, v_wave_err]], file_name="v_wave")

    # read frequencies errors from the frequencies.txt file
    if (OSC_NUM <= 4) and (not FIRST_IS_OPEN) and (not LAST_IS_OPEN):
        with open("frequencies.txt", "r") as freq_file:
            freq_errors = []
            for line in freq_file:
                freq_error = float(line.split("\t")[-2])
                freq_errors.append(freq_error)
            freq_file.close()

        # plot frequency vs dt
        freq_errors_dict = {"freq errors": freq_errors}
        plot_graphs(freq_errors_dict, xAxis_data=DTs, xAxis_title="dt", title="freq_error vs dt", file_name="freq_vs_dt")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  3. Call the function main()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if (__name__ == "__main__") and (RUN == True):
    # To run everything we call the main function.
    main()
    print("Done!")

# If you don't know this if statement __name__ == "__main__" , it's ok.
# In short, it's basically saying - run these following lines only if this file is the main file 
# (not called from another file).
