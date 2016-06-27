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
    This module has a set of useful methods of generic whose is used
    inside of the package MAR.

    * mar.utils.get_firstname
    * mar.utils.get_name
    * mar.utils.save_csv
    * mar.utils.walk
"""

# stdlib
import os
from functools import partial

# self package
import mar


def get_firstname(first, suffix):
    string = ''
    if '_' in first:
        string += first.split('_')[0]
    elif '-' in first:
        string += first.split('-')[0]

    tokens = [string or first, suffix]

    return '-'.join(filter(bool, tokens))


def get_name(path, suffix='report'):
    return get_firstname(os.path.basename(path), suffix)


# this is used on the case when
# the param pass is a directory instead a simple
# csv file
def walk(csvs, ignore_pattern=None):
    root = partial(os.path.join, mar.CURRENT_DIRECTORY)
    files = []
    for csv in csvs:
        if os.path.isdir(csv):
            enter = partial(os.path.join, root(csv))
            files.extend(walk(map(enter, os.listdir(csv))))
        elif any(pattern in csv for pattern in mar.MATCHING_PATTERNS):
            files.append(root(csv))

    if ignore_pattern:
        files = list(filter(lambda x: not ignore_pattern.match(x), files))

    return files


def interval_name(x, period):
    return '{} - {}'.format(str(x * period), (x + 1) * period)
