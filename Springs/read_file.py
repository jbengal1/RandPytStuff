import json

run_num = 1

def read_params(para_file_name):

    with open(para_file_name, "r") as file:
        data = json.load(file)
    file.close()
    
    dt = data['dt']
    l_rest = data['l_rest']
    k = data['k']
    mass = data['mass']
    osc_num = data['osc_num']
    frames_num = data['frames_num']
    first_is_open = data['first_is_open']
    last_is_open = data['last_is_open']
    return dt, l_rest, k, mass, osc_num, frames_num, first_is_open, last_is_open

    '''
    with open(para_file_name, "r") as file:
        for line in file: 
            line = line.split(" = ")
            if line[0]=='dt': dt = float(line[1][:-1])
            elif line[0]=='l_rest': l_rest = float(line[1][:-1])
            elif line[0]=='k': k = float(line[1][:-1])
            elif line[0]=='mass': mass = float(line[1][:-1])
            elif line[0]=='osc_num': osc_num = int(line[1][:-1])
            elif line[0]=='frames_num': frames_num = int(line[1][:-1])
            elif line[0]=='init_displacment': init_displacment = float(line[1][:-1])
            elif line[0]=='err': err = float(line[1][:-1])
            
            elif line[0]=='first_is_open': first_is_open = bool(line[1][:-1])
            elif line[0]=='last_is_open': last_is_open = bool(line[1][:-1])

    return dt, l_rest, k, mass, osc_num, init_displacment, frames_num, init_displacment, first_is_open, last_is_open, err
    '''
