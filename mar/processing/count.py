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


def clusters(dfs, total, groups):
    table = {x: [] for x in groups.keys()}

    for df in tqdm(dfs, total=total):
        # that query is necessary because mar.processing.actions.diff
        # concat malloc & free operations,
        # whose we will has double entries for counting
        df = df.query("type == 'malloc'")
        stats = {x: 0 for x in groups.keys()}
        df['label'] = df['diff'].map(
            lambda x: mar.processing.classify.tag(x, groups))
        for label in df.label:
            stats[label] += 1

        for k, v in stats.items():
            table[k] += [v]

    return pd.DataFrame(table)
