import numpy as np
from numpy import e, pi
from math import factorial
import math
import matplotlib.pyplot as plt


def stirling(n, constant=True):
    answer = (n / e) ** n
    if constant:
        answer *= math.sqrt(2 * pi * n)
    return answer


n = 100
x = np.arange(1, n + 1)
factorial_x = np.array([float(factorial(i)) for i in x])
stirling_x = np.vectorize(stirling)(x)

plt.plot(x, factorial_x, label="factorial", linewidth=2)
plt.plot(x, stirling_x, label="stirling", linestyle="--", linewidth=2)
plt.yscale("log")
plt.legend()
plt.show()
