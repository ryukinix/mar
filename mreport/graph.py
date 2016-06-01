#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

from warnings import warn
from mreport.utils import get_name

try:
    import matplotlib
    from matplotlib import pyplot as plt
    matplotlib.style.use('ggplot')
except:
    warn("Hey, you don't have matplotlib! Install it to get "
         "the matplotlibs plots")


def plot(df, fname, longsize, interval, columns=['longs']):
    ax = df[columns].plot()
    ax.set_ylabel('longs memory releases with {} at least seconds'.format(longsize))
    ax.set_xlabel('Interval clusterized by {} instrunctions'.format(interval))
    plt.legend(loc='upper center')
    plt.title('Memory Analysis of Program {}'.format(get_name(fname)))
    return ax
    

def show(df, fname, longsize, interval, columns=['longs']):
    plot(df, fname, longsize, interval, columns)
    plt.show()


def save(df, fname, longsize, interval, columns=['longs']):
    ax = plot(df, fname, longsize, interval, columns)
    fig = ax.get_figure()
    fig.savefig(fname)
