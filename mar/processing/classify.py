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
    Make usefull classifications about memory like:
        * clusters
        * tag (short, medium, long, undefined)
        * longs

    * mar.processing.classify.clusters
    * mar.processing.classify.tag
    * mar.processing.classify.longs
"""

# self-package
import mar


def tag(diff, groups):
    items = sorted(groups.items(),
                   key=lambda x: x[1].left)
    diff = diff * mar.NANOSECOND  # cast to seconds
    for label, interval in items:
        if diff in interval:
            # print('{diff} -> {label}'.format_map(locals()))
            return label

    return 'undefined'


def longs(df, long_range):
    return df['diff'].map(lambda x: x * mar.NANOSECOND in long_range)
