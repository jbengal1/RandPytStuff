import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import gamma
sns.set_theme(style="darkgrid")

REAL_A = np.array([10, -2])
N = 1000
P = 2
ERR_MAX = 0.1
degreeOfFreedom = N-P
RANGE = [-4, 4]


def h1(t):
    return np.sin(t)**2

def h2(t):
    return t**3


def calcA(meas, err, X):
    # calculate theata parameters vector, by eq (6) in arXive 1012.3754
    Err = np.zeros([len(X), len(X)])
    np.fill_diagonal(Err, err**(-2))
    H = np.array([h1(X), h2(X)]).T
    Left = np.dot(Err, H)
    Left = np.dot(H.T, Left)
    Left = np.linalg.inv(Left)
    Right = np.dot(Err, meas)
    Right = np.dot(H.T, Right)
    return np.dot(Left, Right)
    


def calc_chi_sqr(meas, err , X, fit):
    chi_sqr = 0
    res = []
    for i, t in enumerate(X):
        res.append(meas[i] - fit[i])
        chi_sqr += (res[i]/ err[i]) **2
    
    return res, chi_sqr



x = np.linspace(RANGE[0], RANGE[1], N)
y = np.dot(REAL_A, [h1(x),h2(x)])
sigmas = ERR_MAX * np.random.randn(N)
y += sigmas

A = calcA(y, sigmas, x)
print(A)

fit = np.dot(A, [h1(x), h2(x)])
res, chi = calc_chi_sqr(y, sigmas, x, fit)
# p_val = calc_p_value(chi)
print("chi = ", chi/degreeOfFreedom)

# plt.subplot()
plt.figure(1)
plt.scatter(x, y)
plt.plot(x, fit)
plt.show()

plt.figure(2)
plt.scatter(x, res)
plt.plot(x, np.zeros(len(x)) , 'r')
plt.show()