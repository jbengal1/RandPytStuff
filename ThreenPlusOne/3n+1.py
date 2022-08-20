import matplotlib.pyplot as plt
import numpy as np


def f(x, a):
    if x%2==0:
        a.append(x/2)
        return f(x/2, a)
    elif x==1:
        a.append(1)
        return 1
    else:
        a.append(3*x + 1)
        return f(3*x + 1, a) 

a = []
fig, ax = plt.subplots()  # Create a figure and an axes.
for n in range(1,27):
    arr = []
    f(n, arr)
    a.append(arr)
    x = np.array([i for i in range(0,len(a[n-1]))])
    ax.plot(x ,a[n-1], label = str(n))

plt.show()