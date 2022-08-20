import numpy as np
import matplotlib.pyplot as plt

L = 5
N = 30
alpha = 1
bins = 1000
CUT = 5
h = L/N
y_0, t_0 = 1, 0


def num_integrals(a, b, bins, func):
    arr = np.array([func(a + k*((b-a)/bins)) for k in range(1, bins-1)])
    return ((b-a)/bins)*(func(a)/2 + func(b)/2 + np.sum(arr))

def f(x):
    return x

def a(func):
    return (2/L)*num_integrals(0, L, bins, func)

def u(x, t):
    def fsin(x, n):
        return f(x)*np.sin(n*np.pi*x/L)
    
    arr = np.array([a(n, fsin)*np.sin(n*np.pi*x/L)*np.exp(-((np.pi**2)*(n**2)*alpha/(L**2)) *t) for n in range(1, CUT)])
    return np.sum(arr)
