#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

import os
from functools import partial

from mreport import CURRENT_DIRECTORY
from mreport import MATCHING_PATTERNS
from mreport import processing
from mreport import graph
from mreport.args import parser
from mreport.utils import get_firstname
from decorating import animated


# this is used on the case when
# the param pass is a directory instead a simple
# csv file
def walk(csvs):
    root = partial(os.path.join, CURRENT_DIRECTORY)
    files = []
    for csv in csvs:
        if os.path.isdir(csv):
            enter = partial(os.path.join, root(csv))
            files.extend(walk(map(enter, os.listdir(csv))))
        elif any(pattern in csv for pattern in MATCHING_PATTERNS):
            files.append(root(csv))

    return files


def main():
    options = parser.parse_args()
    with animated('reporting'):
        csvs = walk(options.csvs)
        dfs = processing.parse(csvs)
        with animated('differentiating time'):
            diffs = [processing.diff(m, f) for m, f in dfs]
        del dfs # desalocar memoria para dfs
        sample = diffs[0]
        sample.diff = processing.time_average(diffs)
        del diffs # desalocar as diferenças
        label = partial(processing.long_labelize, limit=options.long)
        sample['long'] = sample['diff'].map(label)
        output_dataframe = processing.stats(sample, options.interval)

    basename = get_firstname(csvs[0])
    if options.show_graph:
        if options.verbose:
            print(":: showing graph")
        graph.show(output_dataframe, basename, options.long, options.interval)
    if options.save_graph:
        figurename = basename + '.jpg'
        graph.save(output_dataframe, figurename, options.long, options.interval)
        if options.verbose:
            print(":: saved graph on: {}".format(figurename))
    if options.verbose:
        print(output_dataframe)

    csvname = basename + '.csv'
    output_dataframe.to_csv(csvname, index=False)
    if options.verbose:
        print(":: saved csv at {}".format(csvname))

if __name__ == '__main__':
    main()
