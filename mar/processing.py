#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

import pandas as pd
import numpy as np
from mar import NANOSECOND
from tqdm import tqdm


def parse(csvs_groups):
    return ((read_malloc(m), read_free(f))
            for m, f in csvs_groups)


def group_csvs(csvs):
    mallocs = sorted(x for x in csvs if 'malloc' in x)
    frees = sorted(x for x in csvs if 'free' in x)
    return list(zip(mallocs, frees))


def remove_nil(df):
    if '(nil)' in df.index:
        return df.drop('(nil)')
    return df


def normalize(df):
    df = remove_nil(df)
    reusage = df.groupby(level=0).cumcount()
    df.index = df.index.map(str) + reusage.map(lambda x: '-' + str(x))
    df.reset_index()
    return df


def load_csv(csv, **kwargs):
    return normalize(pd.read_csv(csv, **kwargs))


def read_malloc(csv, delimiter=';',
                columns=('req', 'time', 'op', 'memory_id'),
                necessary=['time']):
    return load_csv(csv, delimiter=delimiter,
                    names=columns, index_col=3)[necessary]


def read_free(csv, delimiter=' ',
              columns=('time', 'op', 'memory_id'),
              necessary=['time']):
    return load_csv(csv, delimiter=delimiter,
                    names=columns, index_col=2)[necessary]


def diff(malloc, free, by='time'):
    # sync just mallocs whose has free
    malloc = malloc[~free.isin(malloc)].dropna()
    free['type'] = 'free'
    malloc['type'] = 'malloc'
    diff = free[by] - malloc[by]
    free['diff'] = diff
    malloc['diff'] = diff

    return pd.concat([malloc, free]).sort_values(by)


def mean_experiment(diffs, n_experiments, long_range, by='diff'):
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


def classify_long(df, long_range):
    return df['diff'].map(lambda x: x / NANOSECOND in long_range)


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


def count_clusters(diffs):
    return pd.DataFrame()


def interval_name(x, period):
    return '{} - {}'.format(str(x * period), (x + 1) * period)
