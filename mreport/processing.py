#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

import pandas as pd
from decorating import animated
from mreport import MICROSECOND


@animated("parsing csv")
def parse(csvs):
    mallocs = sorted(x for x in csvs if 'malloc' in x)
    frees = sorted(x for x in csvs if 'free' in x)
    return [(read_malloc(malloc),
             read_free(free))
            for malloc, free in zip(mallocs, frees)]


def read_malloc(csv, delimiter=';',
                columns=('req', 'time', 'op', 'memory_id')):
    return pd.read_csv(csv, delimiter=delimiter, names=columns)


def read_free(csv, delimiter=' ',
              columns=('time', 'op', 'memory_id')):
    return pd.read_csv(csv, delimiter=delimiter, names=columns)


@animated("differentiating times")
def diff(malloc, free, by='time', index=['memory_id', 'op']):
    free.sort_values(index, inplace=True)
    malloc.sort_values(index, inplace=True)
    malloc[by] = free[by] - malloc[by]
    return malloc


@animated("labeling")
def labelize(df, limit, label='long'):
    df[label] = df.time.map(lambda x: x / MICROSECOND > limit)
    return df


@animated("average time")
def time_average(diffs, by=['time']):
    average = pd.concat(x[by] for x in diffs)
    return average


def stats(longs, period):
    longs_counter = 0
    longs_memory = 0
    longs_distribution = []
    for i, is_long in enumerate(longs):
        if (i + 1) % 1000 == 0:
            if longs_counter - longs_memory == 0:
                longs_counter = 0
            longs_distribution.append(longs_counter)
            longs_memory = longs_counter

        longs_counter += int(is_long)
    return pd.DataFrame({
        'longs': longs_distribution,
        'interval': [interval_name(x, period) for x in
                     range(len(longs_distribution))]
    })


def interval_name(x, period):
    return '{} - {}'.format(str(x * period), (x + 1) * period)
