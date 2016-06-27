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

# third-lib
import numpy as np

# self-package
import mar


def clusters(df, long_range):
    lp = np.linspace(long_range.left, long_range.right, num=3)
    return df['diff'].map(lambda x: tag(x, lp))


def tag(x, linspace):
    if x >= linspace[2]:
        return 'long'
    elif x >= linspace[1]:
        return 'medium'
    elif x > linspace[0]:
        return 'short'
    else:
        return 'undefined'


def longs(df, long_range):
    return df['diff'].map(lambda x: x * mar.NANOSECOND in long_range)
