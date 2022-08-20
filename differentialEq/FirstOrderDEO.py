import numpy as np
import matplotlib.pyplot as plt

ran = [0, 5]
N = 30
h = (ran[1] - ran[0])/N
y_0, t_0 = 1, 0
a = [0, -1, 0]    
b = [1, 0, 0]   

def analytic_sol(t):
    return np.exp(a[1]*t)

def dervative(t, y, a, b):
    return (a[0] + a[1]*y + a[2]*(y**2))*(b[0] + b[1]*t + b[2]*(t**2))

def t(n):
    return t_0 + h*n 

def y(n):
    if n==0:
        return y_0
    else:
        return y(n-1) + h*dervative(t(n-1), y(n-1), a, b)
 
t_n = np.array([t(n) for n in range(N)])
y_n = np.array([y(n) for n in range(N)])
plt.scatter(t_n, y_n)

y_t = np.array(analytic_sol(t_n))
plt.plot(t_n, y_t)

plt.show()
