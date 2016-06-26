#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright © Manoel Vilela
#
#    @project: Memory Analysis Report
#     @author: Manoel Vilela
#      @email: manoel_vilela@engineer.com
#


from warnings import warn
from mar.utils import get_name
from decorating import animated

try:
    import matplotlib
    from matplotlib import pyplot as plt
    matplotlib.style.use('ggplot')
except:
    warn("Hey, you don't have matplotlib! Install to get the plot working "
         "the matplotlibs plots")


def _plot(df, fname, longsize, interval):
    ax = df.plot()
    ax.set_ylabel('longs ({} s) stack allocation'.format(longsize))
    ax.set_xlabel('Group of {} operations'.format(interval))
    plt.legend(loc='upper center')
    plt.title('Memory Analysis:  {!r}'.format(get_name(fname)).title())
    return ax


def show(df, fname, longsize, interval):
    _plot(df, fname, longsize, interval)
    plt.show()


def save(df, fname, longsize, interval):
    ax = _plot(df, fname, longsize, interval)
    fig = ax.get_figure()
    fig.savefig(fname)


def plot_save(output_dataframe, basename, options):
    if options.show_graph:
        if options.verbose:
            print(":: showing graph")
        with animated("ploting the graph"):
            show(output_dataframe, basename, options.long, options.interval)
    if options.save_graph:
        figurename = basename + '.jpg'
        save(output_dataframe, figurename, options.long, options.interval)
        if options.verbose:
            print(":: saved graph on: {}".format(figurename))
    if options.verbose:
        print(output_dataframe)
