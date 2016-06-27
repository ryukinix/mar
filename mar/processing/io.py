#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright © Manoel Vilela
#
#    @project: Memory Analysis Report
#     @author: Manoel Vilela
#      @email: manoel_vilela@engineer.com
#

"""
    IO module to read, parse and write on disk.

    * mar.processing.io.read_malloc
    * mar.processing.io.read_free
    * mar.processing.io.parse
    * mar.processing.io.group
    * mar.processing.io.load
    * mar.processing.io.save
"""

# third-lib
import pandas as pd
from decorating import animated

# self-package
from mar.processing.normalization import normalize


def read_malloc(csv, nil=False,
                delimiter=';',
                columns=('req', 'time', 'op', 'memory_id'),
                index_col=3,
                necessary=['time']):
    return load(csv, nil=nil, delimiter=delimiter,
                names=columns, index_col=index_col)[necessary]


def read_free(csv, nil=False,
              delimiter=' ',
              columns=('time', 'op', 'memory_id'),
              index_col=2,
              necessary=['time']):
    return load(csv, nil=nil, delimiter=delimiter,
                names=columns, index_col=index_col)[necessary]


def parse(csvs_groups,
          nil=False,
          malloc_columns=['time'],
          free_columns=['time']):
    return ((read_malloc(m, nil, necessary=malloc_columns),
             read_free(f, nil, necessary=free_columns))
            for m, f in csvs_groups)


def group(csvs):
    mallocs = sorted(x for x in csvs if 'malloc' in x)
    frees = sorted(x for x in csvs if 'free' in x)
    return list(zip(mallocs, frees))


def load(csv, nil=False, **kwargs):
    return normalize(pd.read_csv(csv, **kwargs), nil=nil)


def save(output_dataframe, basename, verbose=False):
    with animated("saving output on csv"):
        csvname = basename + '.csv'
        output_dataframe.to_csv(csvname, index=False)
        if verbose:
            print(":: saved csv at {}".format(csvname))
