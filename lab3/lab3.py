#!/usr/bin/env python

from sin_plot import plot_sin
from histo_plot import plot_histo
from spring_mass_plot import plot_spring_mass
from sort_sum_plot import plot_sort_sum


def show_plots():
    plot_sin()
    plot_histo()
    plot_spring_mass()
    plot_sort_sum()


if __name__ == '__main__':
    show_plots()
