import random
from math import *
import json
from read_file import read_params


def initial_grid():
    x_s = [0]*osc_num
    v_s = [0]*osc_num
    print(l_rest)
    for i in range(1, osc_num):
        x_s[i] = x_s[0] + l_rest*i

    return x_s, v_s


def initial_conditions1(x_s):
    x_s[1] += init_displacment


def initial_conditions2_opposite(x_s):
    x_s[1] -= init_displacment
    x_s[2] += init_displacment


def initial_conditions2_same(x_s):
    x_s[1] += init_displacment
    x_s[2] += init_displacment


def initial_conditions_N(x_s):
    for i in range(1, osc_num-1):
        if i%2==0:
            x_s[i] += init_displacment
        else:
            x_s[i] -= init_displacment


def initial_conditions_wave(x_s):
    # Left osc is moved while others are at the self mode state
    x_s[0] -= 2*init_displacment

def initial_conditions_random(x_s):
    # All oscs are moved randomly
    # x_s[0] = 2*(random.randint(-50,50)/25)*init_displacment
    for i, x in enumerate(x_s):
        x_s[i] += 2*(random.randint(-50,50)/25)*init_displacment


def write_to_file(file_name):
    with open(file_name, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    '''
    with open(file_name, "w") as file:
        file.write("x_init" + "\t")
        for x in x_s:
            file.write(str(x) + "\t")
        file.write("\n")

        file.write("v_init" + "\t")
        for v in v_s:
            file.write(str(v) + "\t")
    '''


para_file_name = [f"input_parameters{i}.json" for i in range(1, 10)]
state_file_name = [f"input_initState{i}.json" for i in range(1, 10)]

dt, l_rest, k, mass, osc_num, frames_num, first_is_open, last_is_open = read_params(para_file_name[0])
init_displacment = 1
x_s, v_s = initial_grid()
initial_conditions1(x_s)

data = {"x":x_s, "v":v_s}
write_to_file(state_file_name[0])

dt, l_rest, k, mass, osc_num, frames_num, first_is_open, last_is_open = read_params(para_file_name[1])
init_displacment = 1
x_s, v_s = initial_grid()
initial_conditions2_same(x_s)
data = {"x":x_s, "v":v_s}
write_to_file(state_file_name[1])

dt, l_rest, k, mass, osc_num, frames_num, first_is_open, last_is_open = read_params(para_file_name[2])
init_displacment = 1
x_s, v_s = initial_grid()
initial_conditions2_opposite(x_s)
data = {"x":x_s, "v":v_s}
write_to_file(state_file_name[2])

dt, l_rest, k, mass, osc_num, frames_num, first_is_open, last_is_open = read_params(para_file_name[3])
x_s, v_s = initial_grid()
init_displacment = 1
initial_conditions_N(x_s)
data = {"x":x_s, "v":v_s}
write_to_file(state_file_name[3])

dt, l_rest, k, mass, osc_num, frames_num, first_is_open, last_is_open = read_params(para_file_name[4])
init_displacment = 1
x_s, v_s = initial_grid()
initial_conditions_wave(x_s)
data = {"x":x_s, "v":v_s}
write_to_file(state_file_name[4])

dt, l_rest, k, mass, osc_num, frames_num, first_is_open, last_is_open = read_params(para_file_name[5])
init_displacment = 1
x_s, v_s = initial_grid()
initial_conditions_wave(x_s)
data = {"x":x_s, "v":v_s}
write_to_file(state_file_name[5])

dt, l_rest, k, mass, osc_num, frames_num, first_is_open, last_is_open = read_params(para_file_name[6])
init_displacment = 1
x_s, v_s = initial_grid()
initial_conditions_random(x_s)
data = {"x":x_s, "v":v_s}
write_to_file(state_file_name[6])

dt, l_rest, k, mass, osc_num, frames_num, first_is_open, last_is_open = read_params(para_file_name[7])
init_displacment = 1
x_s, v_s = initial_grid()
initial_conditions_random(x_s)
data = {"x":x_s, "v":v_s}
write_to_file(state_file_name[7])