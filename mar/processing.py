#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright © Manoel Vilela
#
#    @project: Memory Analysis Report
#     @author: Manoel Vilela
#      @email: manoel_vilela@engineer.com
#

# third-lib
import numpy as np
import pandas as pd
from tqdm import tqdm

# self-package
import mar


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


def remove_nil(df):
    if '(nil)' in df.index:
        return df.drop('(nil)')
    return df


def normalize(df, nil=False):
    if not nil:
        df = remove_nil(df)
    reusage = df.groupby(level=0).cumcount()
    df.index = df.index.map(str) + reusage.map(lambda x: '-' + str(x))
    df.reset_index()
    return df


def load_csv(csv, nil=False, **kwargs):
    return normalize(pd.read_csv(csv, **kwargs), nil=nil)


def read_malloc(csv, nil=False,
                delimiter=';',
                columns=('req', 'time', 'op', 'memory_id'),
                index_col=3,
                necessary=['time']):
    return load_csv(csv, nil=nil, delimiter=delimiter,
                    names=columns, index_col=index_col)[necessary]


def read_free(csv, nil=False,
              delimiter=' ',
              columns=('time', 'op', 'memory_id'),
              index_col=2,
              necessary=['time']):
    return load_csv(csv, nil=nil, delimiter=delimiter,
                    names=columns, index_col=index_col)[necessary]


def diff(malloc, free, by='time'):
    # sync just mallocs whose has free
    malloc = malloc[~free.isin(malloc)].dropna()
    free['type'] = 'free'
    malloc['type'] = 'malloc'
    diff = free[by] - malloc[by]
    free['diff'] = diff
    malloc['diff'] = diff

    return pd.concat([malloc, free]).sort_values(by)


def merge(malloc, free, sorting_by='time'):
    malloc = malloc[~free.isin(malloc)].dropna()
    free['type'] = 'free'
    malloc['type'] = 'malloc'
    return pd.concat([malloc, free]).sort_values(sorting_by)


def remove_zeros(malloc, column='req'):
    for index in malloc.index:
        if int(malloc.loc[index][column]) == 0:
            malloc.drop(index)
    return malloc


def mean(diffs, n_experiments, long_range, by='diff'):
    smp = next(diffs)
    times = smp[by]
    for index, df in tqdm(enumerate(diffs), total=n_experiments, initial=1):
        times = pd.Series(x + y for x, y in zip(times, df[by]))
    smp.diff = times / n_experiments
    return smp


def clusterize(x, linspace):
    if x >= linspace[2]:
        return 'long'
    elif x >= linspace[1]:
        return 'medium'
    elif x > linspace[0]:
        return 'short'
    else:
        return 'undefined'


def classify_longs(df, long_range):
    return df['diff'].map(lambda x: x / mar.NANOSECOND in long_range)


def classify_clusters(df, long_range):
    lp = np.linspace(long_range.left, long_range.right, num=3)
    return df['diff'].map(lambda x: clusterize(x, lp))


def count_longs(df, period):
    longs_stack = 0
    longs_distribution = []
    values = tqdm(enumerate(zip(df.long, df.type)),
                  total=len(df.index))
    for i, (is_long, op_type) in values:
        if (i + 1) % 1000 == 0:
            longs_distribution.append(longs_stack)
        signal = 1 if op_type == 'malloc' else -1
        longs_stack += signal * int(is_long)
    return pd.DataFrame(dict(longs=longs_distribution,
                             interval=[interval_name(x, period) for x in
                                       range(len(longs_distribution))]))


def count_clusters(diffs, n_experiments, long_range):
    table = dict(short=[],
                 medium=[],
                 long=[],
                 undefined=[])

    for diff in tqdm(diffs, total=n_experiments):
        stats = dict(short=0,
                     medium=0,
                     long=0,
                     undefined=0)
        diff.label = classify_clusters(diff, long_range)
        for label in tqdm(diff.label):
            stats[label] += 1

        for k, v in stats.items():
            table[k] += [v]

    return pd.DataFrame(table)


def interval_name(x, period):
    return '{} - {}'.format(str(x * period), (x + 1) * period)
