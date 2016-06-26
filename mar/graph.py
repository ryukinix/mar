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


def _plot(df, fname, x_label, y_label):
    ax = df.plot()
    ax.set_ylabel(x_label)
    ax.set_xlabel(y_label)
    plt.legend(loc='upper right')
    plt.title('Memory Analysis:  {!r}'.format(get_name(fname)).title())
    return ax


def show(df, fname, x_label, y_label):
    _plot(df, fname, x_label, y_label)
    plt.show()


def save(df, fname, x_label, y_label):
    ax = _plot(df, fname, x_label, y_label)
    fig = ax.get_figure()
    fig.savefig(fname)


def plot_save(output_dataframe, basename, options,
              x_label='Stack allocation',
              y_label='Operations in execution by time'):
    verbose = False
    if 'verbose' in options and options.verbose:
        verbose = True
    if options.show_graph:
        if verbose:
            print(":: showing graph")
        with animated("ploting the graph"):
            show(output_dataframe, basename, x_label, y_label)
    if options.save_graph:
        figurename = basename + '.jpg'
        save(output_dataframe, figurename, x_label, y_label)
        if verbose:
            print(":: saved graph on: {}".format(figurename))
    if verbose:
        print(output_dataframe)
