#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

import pandas as pd
from mreport import NANOSECOND
from tqdm import tqdm


def parse(csvs):
    mallocs = sorted(x for x in csvs if 'malloc' in x)
    frees = sorted(x for x in csvs if 'free' in x)
    return [(read_malloc(malloc),
             read_free(free))
            for malloc, free in tqdm(zip(mallocs, frees), total=len(csvs)//2)]


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
    malloc = malloc[~free.isin(malloc)].dropna()
    free['type'] = 'free'
    malloc['type'] = 'malloc'
    diff = free[by] - malloc[by]
    free['diff'] = diff
    malloc['diff'] = diff

    return pd.concat([malloc, free]).sort_values(by)


def long_labelize(x, limit=1):
    return x / NANOSECOND > limit


def time_average(diffs, by='diff'):
    experiments = len(diffs)
    times = diffs[0][by]
    for index, df in enumerate(tqdm(diffs, total=len(diffs))):
        times = pd.Series(x + y for x, y in zip(times, df[by]))
    return times / experiments


def stats(df, period):
    longs_stack = 0
    longs_distribution = []
    for i, (is_long, op_type) in tqdm(enumerate(zip(df.long, df.type)), total=len(df.index)):
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
