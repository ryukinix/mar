#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

import os
import re
from functools import partial

from mar import CURRENT_DIRECTORY
from mar import MATCHING_PATTERNS
from mar import processing
from mar import graph
from mar.args import parser
from mar.utils import get_firstname
from tqdm import tqdm
from decorating import animated


# this is used on the case when
# the param pass is a directory instead a simple
# csv file
def walk(csvs, ignore_pattern=None):
    root = partial(os.path.join, CURRENT_DIRECTORY)
    files = []
    for csv in csvs:
        if os.path.isdir(csv):
            enter = partial(os.path.join, root(csv))
            files.extend(walk(map(enter, os.listdir(csv))))
        elif any(pattern in csv for pattern in MATCHING_PATTERNS):
            files.append(root(csv))

    if ignore_pattern:
        files = list(filter(lambda x: not ignore_pattern.match(x), files))

    return files


def main():
    options = parser.parse_args()
    if options.ignore_first:
        options.ignore = re.compile('.*_1.csv')

    csvs = walk(options.csvs, options.ignore)
    groups = processing.group_csvs(csvs)
    dfs = processing.parse(groups)
    diffs = (processing.diff(m, f) for m, f in dfs)
    print(":: dynamic evaluating experiments")
    print(":: load csv -> differentiating -> mean -> tagging longs")
    processed = processing.eval_experiment(diffs, n_experiments=len(groups), 
                                           long_size=options.long)
    print(":: counting longs ")
    output_dataframe = processing.stats(processed, options.interval)

    basename = get_firstname(csvs[0])
    if options.show_graph:
        if options.verbose:
            print(":: showing graph")
        with animated("ploting the graph"):
            graph.show(output_dataframe, basename, options.long, options.interval)
    if options.save_graph:
        figurename = basename + '.jpg'
        graph.save(output_dataframe, figurename, options.long, options.interval)
        if options.verbose:
            print(":: saved graph on: {}".format(figurename))
    if options.verbose:
        print(output_dataframe)

    with animated("saving output on csv"):
        csvname = basename + '.csv'
        output_dataframe.to_csv(csvname, index=False)
        if options.verbose:
            print(":: saved csv at {}".format(csvname))

if __name__ == '__main__':
    main()