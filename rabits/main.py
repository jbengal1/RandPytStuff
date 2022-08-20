
import numpy as np
import matplotlib.pyplot as plt

def x(n, a):
    if n==0:
        return 0.5
    else:
        return a*x(n-1, a)*(1 - x(n-1, a))

N = 10
fig_num = 4
fig, axs = plt.subplots(int(fig_num/2), int(fig_num/2))
x_arr = np.linspace(1,N,N)

for a in range(1,fig_num+1):
    y_arr = np.array([x(n, a) for n in range(N)])
    row = int(fig_num/2)%a
    col = int(fig_num/2)%a + (a - 1)

    axs[row,col].scatter(x_arr, y_arr)
    axs[row,col].set_ylabel('# rabits')
    axs[row,col].set_xlabel('generation')
    axs[row,col].text(0.5,0.25, r'a = ' + str(a), horizontalalignment='center')
    axs[row,col].grid(True)

plt.show()

