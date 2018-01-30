#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from math import pi


def plot_sin():
    rng = np.arange(0, 4*pi, pi / 25)
    plt.plot(rng, np.sin(rng))
    plt.title("A Sin Curve")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


if __name__ == '__main__':
    plot_sin()
