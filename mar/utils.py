#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright © Manoel Vilela
#
#    @project: Memory Analysis Report
#     @author: Manoel Vilela
#      @email: manoel_vilela@engineer.com
#

# stdlib
import os
from functools import partial

# third-package
from decorating import animated

# self package
import mar


def get_firstname(first, suffix='report'):
    string = ''
    if '_' in first:
        string += first.split('_')[0]
    elif '-' in first:
        string += first.split('-')[0]

    tokens = [string or first, suffix]

    return '-'.join(filter(bool, tokens))


def get_name(path):
    return get_firstname(os.path.basename(path), suffix='')


def save_csv(output_dataframe, basename, options):
    with animated("saving output on csv"):
        csvname = basename + '.csv'
        output_dataframe.to_csv(csvname, index=False)
        if options.verbose:
            print(":: saved csv at {}".format(csvname))


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
