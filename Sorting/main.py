from datetime import time
import numpy as np
import time
import matplotlib.pyplot as plt

plt.figure()



# numpy version
N = []
dt = []
pow = 5
for n in range(1,pow):
    N.append(10**n)
    arr = np.random.randint(N[n-1], size=N[n-1])
    
    init_time = time.time()
    a = np.sort(arr)
    final_time = time.time()
    
    dt.append( final_time - init_time)

plt.scatter(N, dt)



# my version
def switch(arr, i):
    temp = arr[i+1]
    arr[i+1] = arr[i]
    arr[i] = temp

sorted = False
    
def avg(arr):
    sum = 0
    for x in arr:
        sum +=x
    return sum/len(arr)

def sort(arr, arr_size):

    while not sorted:
        counter = 0

        for i in range(len(arr) -1 ):
            if arr[i] > arr[i+1]:
                switch(arr, i)
                counter+=1
        
        if counter==0:  sorted = True


N_my = []
dt_my = []
pow = 5
for n in range(1,pow):
    N_my.append(10**n)
    arr = np.random.randint(N_my[n-1], size=N_my[n-1])
    init_time = time.time()
    sort(arr)
    final_time = time.time()
    
    dt_my.append(final_time - init_time)
    #print(arr)

plt.scatter(N_my, dt_my)
plt.grid(1)
plt.xscale("log")
plt.yscale("log")
plt.show()
