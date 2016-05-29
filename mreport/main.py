#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

import os

from mreport import CURRENT_DIRECTORY
from mreport import processing
from mreport import graph
from mreport.args import parser
from decorating import animated


# this is used on the case when
# the param pass is a directory instead a simple
# csv file
def normalize_arguments(csvs):
    files = []
    for csv in csvs:
        if os.path.isdir(csv):
            files.append(os.readir(csv))
        else:
            files.append(os.path.join(CURRENT_DIRECTORY, csv))

    return files


def get_basename(first):
    try:
        return first.split('_')[0] + '-report'
    except:
        return 'report'


@animated("reporting")
def main():
    options = parser.parse_args()
    csvs = normalize_arguments(options.csvs)
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
