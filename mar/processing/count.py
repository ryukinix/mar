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
    Do count of longs (above limit) and clusters (short/mid/long):

    * mar.processing.count.longs
    * mar.processing.count.clusters
"""

# third-lib
import pandas as pd
from tqdm import tqdm

# self-package
import mar


def longs(df, interval):
    stack = 0
    distribution = []
    values = tqdm(enumerate(zip(df.long, df.type)),
                  total=len(df.index))
    for i, (is_long, op_type) in values:
        if (i + 1) % interval == 0:
            distribution.append(stack)
        signal = 1 if op_type == 'malloc' else -1
        stack += signal * int(is_long)
    return pd.DataFrame(dict(longs=distribution,
                             interval=[mar.utils.interval_name(x, interval)
                                       for x in range(len(distribution))]))


def clusters(diffs, total, long_range):
    table = dict(short=[],
                 medium=[],
                 long=[],
                 undefined=[])

    for diff in tqdm(diffs, total=total):
        stats = dict(short=0,
                     medium=0,
                     long=0,
                     undefined=0)
        diff.label = mar.processing.classify.clusters(diff, long_range)
        for label in tqdm(diff.label):
            stats[label] += 1

        for k, v in stats.items():
            table[k] += [v]

    return pd.DataFrame(table)
