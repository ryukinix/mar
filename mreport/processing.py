#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

import pandas as pd


def parse(csvs):
    mallocs = sorted(x for x in csvs if 'malloc' in x)
    frees = sorted(x for x in csvs if 'free' in x)
    dfs = zip(mallocs, frees)
    return [(pd.read_csv(m), pd.read_csv(f)) for m, f in dfs]


def diff(malloc, free, by='time', index='memory_id',
         m_columns=('req', 'op', 'memory_id'),
         f_columns=('op', 'memory_id')):
    malloc.sort_values(index, inplace=True)
    free.sort_values(index, inplace=True)
    df_diff = pd.merge(malloc, free)
    df_diff[by] = (malloc[by] - free[by])
    return df_diff


def labelize(df, limit, label='long'):
    df[label] = df.time.map(lambda x: x > limit / 1000)
    return df


def average(dfs, by='time'):
    return pd.merge([x[by] for x in dfs]).mean(axis=1)[by]


def stats(dfs, slice):
    pass
