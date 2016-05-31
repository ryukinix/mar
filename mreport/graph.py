#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

from warnings import warn

try:
    import matplotlib
    from matplotlib import pyplot as plt
    matplotlib.style.use('ggplot')
except:
    warn("Hey, you don't have matplotlib! Install it to get "
         "the matplotlibs plots")


def show(df, columns=['longs']):
    df[columns].plot()
    plt.show()


def save(df, fname, columns=['longs']):
    ax = df[columns].plot()
    fig = ax.get_figure()
    fig.savefig('asdf.png')
