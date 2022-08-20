import numpy as np

particle_number = 100
volume = [100, 100]
time_interval = 100
time = np.linspace(0, time_interval, time_interval)

def get_particle_number():
    return particle_number

def get_volume():
    return volume

def get_time():
    return time