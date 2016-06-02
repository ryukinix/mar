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
from decorating import animated
from mreport import NANOSECOND


@animated("parsing csv")
def parse(csvs):
    mallocs = sorted(x for x in csvs if 'malloc' in x)
    frees = sorted(x for x in csvs if 'free' in x)
    return [(read_malloc(malloc),
             read_free(free))
            for malloc, free in zip(mallocs, frees)]


def remove_nil(df):
    if '(nil)' in df.index:
        return df.drop('(nil)')
    return df


def normalize(df):
    df = remove_nil(df)
    df['re-usage'] = df.groupby(level=0).cumcount()
    return df.set_index('re-usage', append=True)


def load_csv(csv, **kwargs):
    return normalize(pd.read_csv(csv, **kwargs))


def read_malloc(csv, delimiter=';',
                columns=('req', 'time', 'op', 'memory_id'),
                necessary=['time', 'op']):
    return load_csv(csv, delimiter=delimiter,
                    names=columns, index_col=[3])[necessary]


def read_free(csv, delimiter=' ',
              columns=('time', 'op', 'memory_id'),
              necessary=['time', 'op']):
    return load_csv(csv, delimiter=delimiter,
                    names=columns, index_col=[2])[necessary]


def diff(malloc, free, by='time'):
    free['type'] = 'free'
    malloc['type'] = 'malloc'
    free['diff'] = np.NaN
    malloc['diff'] = np.NaN
    free.sort_values(by, inplace=True)
    malloc.sort_values(by, inplace=True)

    for label in free.index:
        time_diff = free.loc[label, by] - malloc.loc[label, by]
        free.loc[label, 'diff'] = time_diff
        malloc.loc[label, 'diff'] = time_diff

    return pd.concat([free, malloc]).sort_values(by).dropna(how='any')


def labelize(df, limit, label='long'):
    df[label] = df['diff'].map(lambda x: x / NANOSECOND > limit)
    return df


@animated('time average')
def time_average(diffs, by='diff'):
    experiments = len(diffs)
    times = diffs[0][by]
    for index, df in enumerate(diffs):
        times = pd.Series(x + y for x, y in zip(times, df[by]))
    return times / experiments


def stats(df, period):
    longs_stack = 0
    longs_distribution = []
    print(df)
    for i, (is_long, op_type) in enumerate(zip(df.long, df.type)):
        if (i + 1) % 1000 == 0:
            longs_distribution.append(longs_stack)
        signal = 1 if op_type == 'malloc' else -1
        longs_stack += signal * int(is_long)
    return pd.DataFrame({
        'longs': longs_distribution,
        'interval': [interval_name(x, period) for x in
                     range(len(longs_distribution))]
    })


def interval_name(x, period):
    return '{} - {}'.format(str(x * period), (x + 1) * period)
