from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

# number of simulations
N = 100

average_increase = 4.48/100
std = 15/100

years = 0
months = 12
overall_months = months + int(years/12) 

init_inv = 10000
monthly_inv = 0

fin_sum = np.array([])
fin_yield_arr = np.array([])
monthly_sum_arr = np.empty((overall_months, N))

for n in range(N):
    percentege = np.random.normal(average_increase, std, overall_months)
    
    monthly_sum = np.array([init_inv])
    monthly_sum_arr[0, n] = init_inv
    for month in range(overall_months):        
        monthly_sum = np.append(monthly_sum, monthly_sum[-1]*(1 + percentege[month]) + monthly_inv)
        monthly_sum_arr[month, n] = monthly_sum[-1]

    fin_sum = np.append(fin_sum, monthly_sum[-1])
    fin_yield_perc =  ((monthly_sum[-1] - (init_inv + monthly_inv*overall_months))/init_inv)*100
    fin_yield_arr =  np.append(fin_yield_arr, fin_yield_perc)

print(np.mean(fin_sum), np.std(fin_sum))
print(np.mean(fin_yield_arr), np.std(fin_yield_arr))
print(fin_sum[fin_sum<0])
plt.hist(fin_sum)
# plt.show()

num_fig = int(sqrt(N))
fig, axs = plt.subplots(num_fig, num_fig)
x = np.linspace(0, overall_months, overall_months)

fig_num = 0
for n in range(num_fig):
    for m in range(num_fig):
        axs[n, m].plot(x, monthly_sum_arr[:, fig_num])
        axs[n, m].set_title(f'{n}, {m}')
        fig_num += 1

plt.show()