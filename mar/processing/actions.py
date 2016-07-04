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

    A collection of actions to handle memory debug dataframes

    * mar.processing.actions.diff
    * mar.processing.actions.merge
    * mar.processing.actions.mean

"""

# third-lib
import pandas as pd
from tqdm import tqdm


def alloc_sync(malloc, free):
    """sync just mallocs whose has free"""
    return malloc[~free.isin(malloc)].dropna()


def diff(malloc, free, by='time'):
    malloc = alloc_sync(malloc, free)
    free['type'] = 'free'
    malloc['type'] = 'malloc'
    diff = free[by] - malloc[by]
    free['diff'] = diff
    malloc['diff'] = diff

    return pd.concat([malloc, free]).sort_values(by)


def merge(malloc, free):
    malloc = alloc_sync(malloc, free)
    free['type'] = 'free'
    malloc['type'] = 'malloc'
    return pd.concat([malloc, free])


def mean(diffs, total, by='diff'):
    smp = next(diffs)
    times = smp[by]
    for index, df in tqdm(enumerate(diffs), total=total, initial=1):
        times = pd.Series(x + y for x, y in zip(times, df[by]))
    smp.diff = times / total
    return smp
