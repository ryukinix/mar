#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

from warnings import warn
from mar.utils import get_name

try:
    import matplotlib
    from matplotlib import pyplot as plt
    matplotlib.style.use('ggplot')
except:
    warn("Hey, you don't have matplotlib! Install to get the plot working "
         "the matplotlibs plots")


def _plot(df, fname, longsize, interval, columns=['longs']):
    ax = df[columns].plot()
    ax.set_ylabel('longs ({} s) stack allocation'.format(longsize))
    ax.set_xlabel('Group of {} operations'.format(interval))
    plt.legend(loc='upper center')
    plt.title('Memory Analysis:  {!r}'.format(get_name(fname)).title())
    return ax
    

def show(df, fname, longsize, interval, columns=['longs']):
    _plot(df, fname, longsize, interval, columns)
    plt.show()


def save(df, fname, longsize, interval, columns=['longs']):
    ax = _plot(df, fname, longsize, interval, columns)
    fig = ax.get_figure()
    fig.savefig(fname)
