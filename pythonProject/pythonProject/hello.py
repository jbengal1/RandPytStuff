import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 100)
y = x**2

plt.plot(x, y)
plt.show()

plt.savefig("plot_test.png")
