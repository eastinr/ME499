#!/usr/bin/env python

import msd
import matplotlib.pyplot as plt


def plot_spring_mass():
    smd = msd.MassSpringDamper(m=10.0, k=10.0, c=1.0)
    state, t = smd.simulate(0.0, 1.0)

    plt.plot(t, state[:,0])
    plt.title("Mass Position Vs. Time")
    plt.xlabel("Time")
    plt.ylabel("Position")
    plt.show()


if __name__ == '__main__':
    plot_spring_mass()
