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
                columns=('req', 'time', 'op', 'memory_id')):
    return load_csv(csv, delimiter=delimiter, names=columns)


def read_free(csv, delimiter=' ',
              columns=('time', 'op', 'memory_id')):
    return load_csv(csv, delimiter=delimiter, names=columns)


def diff(malloc, free, by='time', index=['memory_id', 'op']):
    free.sort_values(index, inplace=True)
    malloc.sort_values(index, inplace=True)
    malloc[by] = free[by] - malloc[by]
    return malloc


def labelize(df, limit, label='long'):
    df[label] = df.time.map(lambda x: x / NANOSECOND > limit)
    return df


@animated('time average')
def time_average(diffs, by=['time']):
    average = pd.concat(x[by] for x in diffs)
    return average


def stats(longs, period):
    longs_counter = 0
    longs_memory = 0
    longs_distribution = []
    interval = 0
    for i, is_long in enumerate(longs):
        if (i + 1) % 1000 == 0:
            if interval == 0:
                longs_counter = longs_memory
            else:
                longs_counter = interval

            longs_distribution.append(longs_counter)
            longs_memory = longs_counter

        interval += int(is_long)
    return pd.DataFrame({
        'longs': longs_distribution,
        'interval': [interval_name(x, period) for x in
                     range(len(longs_distribution))]
    })


def interval_name(x, period):
    return '{} - {}'.format(str(x * period), (x + 1) * period)
