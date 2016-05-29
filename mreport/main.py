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


def get_basename(first):
    try:
        return first.split('_')[0] + '-report'
    except:
        return 'report'


def main():
    options = parser.parse_args()
    with animated('reporting'):
        csvs = walk(options.csvs)
        dfs = processing.parse(csvs)
        diffs = [processing.diff(m, f) for m, f in dfs]
        sample = diffs[0]
        sample.time = processing.time_average(diffs)
        labeled = processing.labelize(sample, options.long)
        output = processing.stats(labeled['long'], options.interval)

    basename = get_basename(csvs[0])
    if options.show_graph:
        graph.show(output)
    if options.save_graph:
        graph.save(output, basename + '.jpg')
    if options.verbose:
        print(output)

    output.to_csv(basename + '.csv', index=False)

if __name__ == '__main__':
    main()
