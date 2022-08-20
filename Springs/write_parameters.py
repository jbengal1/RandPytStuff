from math import *
import numpy as np
import json

para_file_name = [f"input_parameters{i}.json" for i in range(1, 10)]


def write_to_file(data, filename):
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def update_dt(data, T):
    dt = [0 for n in range(len(data["frames_num"]))]
    i = 0
    for frames in data["frames_num"]:
        time = np.linspace(0, 4*T, frames)
        dt[i] = round(time[1] - time[0], 5)
        i += 1
    data["dt"] = dt


# frames_num = [int(n**4) for n in range(2, 15)]
frames_num = [int(n**2.5) for n in range(3, 25)]
print(frames_num)
l_rest = 10
k = 4
mass = 1
omega = sqrt(2*k/mass)
T = 2*pi/omega

# Write the data to dictonary
data = {
    "frames_num": frames_num,
    "dt": 0.1,
    "l_rest": l_rest,
    "k": k,
    "mass": mass,
    "omega": omega,
    "osc_num": 3,
    "first_is_open": False,
    "last_is_open": False
}

update_dt(data, T)
print(data["dt"])


# File 1
write_to_file(data, para_file_name[0])

# Files 2
data["osc_num"] = 4
data["frames_num"] = [400]
data["omega"] = sqrt(k/mass)
update_dt(data, T)
write_to_file(data,para_file_name[1])

# Files 3
data["omega"] = sqrt(3*k/mass)
write_to_file(data,para_file_name[2])

# File 4
data["osc_num"] = 20
data["first_is_open"] = True
data["last_is_open"] = True
data["frames_num"] = [1000]
data["k"] = 6
data["l_rest"] = data["l_rest"]*0.75
data["mass"] = 1.4
data["omega"] = None

k = 0.01 # This is the wave number now. Not sure what it should be though :P

omega = sqrt(data["k"]/data["mass"])*k*data["l_rest"]
print(omega)
T = 2*pi/omega
update_dt(data, T)
write_to_file(data,para_file_name[3])

# File 5
data["osc_num"] = 800
data["first_is_open"] = True
data["last_is_open"] = True
data["frames_num"] = [5000]
data["omega"] = None

C_s = omega/k
T = (data["l_rest"]*data["osc_num"])/C_s
update_dt(data, T)
write_to_file(data,para_file_name[4])

# File 6
data["osc_num"] = 110
data["first_is_open"] = True
data["last_is_open"] = True
data["frames_num"] = [1000]
data["omega"] = None
data["l_rest"] = 10

update_dt(data, T)
data["dt"] = [0.1]
write_to_file(data, para_file_name[5])

# File 7
data["osc_num"] = 3
data["first_is_open"] = True
data["last_is_open"] = True
data["frames_num"] = [1000]
data["omega"] = None
data["l_rest"] = 10

update_dt(data, T)
data["dt"] = [0.1]
write_to_file(data, para_file_name[6])

# File 8
data["osc_num"] = 50
data["first_is_open"] = True
data["last_is_open"] = True
data["frames_num"] = [3000]
data["omega"] = None
data["l_rest"] = 10

update_dt(data, T)
data["dt"] = [0.1]
write_to_file(data, para_file_name[7])