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


def nil_nan(x):
    return np.NaN if x == '(nil)' else x


def normalize(df):
    return df.applymap(nil_nan).dropna(how='any')


def load_csv(csv, **kwargs):
    return normalize(pd.read_csv(csv, **kwargs))


def read_malloc(csv, delimiter=';',
                columns=('req', 'time', 'op', 'memory_id'),
                necessary=['time', 'memory_id', 'op']):
    return load_csv(csv, delimiter=delimiter, names=columns)[necessary]


def read_free(csv, delimiter=' ',
              columns=('time', 'op', 'memory_id'),
              necessary=['time', 'memory_id', 'op']):
    return load_csv(csv, delimiter=delimiter, names=columns)[necessary]


def diff(malloc, free, by='time', index='memory_id'):
    free.sort_values(index, inplace=True)
    malloc.sort_values(index, inplace=True)
    free['type'] = 'free'
    malloc['type'] = 'malloc'
    free['diff'] = np.NaN
    malloc['diff'] = np.NaN
    for m_i, m in enumerate(malloc[index]):
        for f_i, f in enumerate(free[index]):
            if f == m:
                print('freeee')
                diff = malloc[by][m_i] - free[by][f_i]
                malloc.loc[m_i] = diff
                free.loc[f_i] = diff
                break
            if f > m:
                break

    return pd.concat([free, malloc]).sort_values('time').dropna(how='any')


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
