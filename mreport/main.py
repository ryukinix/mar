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

from mreport import CURRENT_DIRECTORY
from mreport import MATCHING_PATTERNS
from mreport import processing
from mreport import graph
from mreport.args import parser
from mreport.utils import get_firstname
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
        ignore = re.compile(ignore_pattern)
        files = list(filter(lambda x: not ignore.match(x), files))

    return files


def main():
    options = parser.parse_args()
    if options.ignore_first:
        options.ignore = '.*1.csv'

    print(":: parsing csvs")
    csvs = walk(options.csvs, options.ignore)
    dfs = processing.parse(csvs)
    print(":: differentiating free-malloc time on experiments")
    diffs = [processing.diff(m, f) for m, f in tqdm(dfs)]
    del dfs  # desalocar memoria para dfs
    sample = diffs[0]
    print(":: doing the average diff between the experiments")
    sample.diff = processing.time_average(diffs)
    del diffs  # desalocar as diferenças
    label = partial(processing.long_labelize, limit=options.long)
    sample['long'] = sample['diff'].map(label)
    print(":: calculating longs")
    output_dataframe = processing.stats(sample, options.interval)

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
