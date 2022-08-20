import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N = 100


def solve_analytic(x, y):
    b = np.sum((x - np.mean(x))*(y - np.mean(y))) / np.sum((x - np.mean(x))**2)
    a = np.mean(y) - b*np.mean(x)
    return np.array([a, b])


def main():
    a = 0.5
    b = 1
    x = np.linspace(0, 1, N)
    true_value = a*x + b
    training = true_value + 0.5*(np.random.rand(N) - 0.5)

    w = solve_analytic(x, training)
    y = w[0]+ w[1]*x

    rms = np.abs(true_value - training)
    mse = np.sum(rms**2) / N
    rmse = np.sqrt(mse)
    rse = np.sum((training - y)**2)/np.sum((training - np.mean(training))**2)
    print(mse)
    print(rmse)
    print(1-rse)

    fig, ax = plt.subplots()
    ax.plot(x, true_value, label='true value')
    ax.errorbar(x, y, yerr=rms,label='analytic solution')
    ax.scatter(x, training, label='with noise')
    ax.legend()
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
