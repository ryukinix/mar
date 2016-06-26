#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright © Manoel Vilela
#
#    @project: Memory Analysis Report
#     @author: Manoel Vilela
#      @email: manoel_vilela@engineer.com
#

import re

from mar import processing
from mar import graph
from mar import utils


def main():
    from mar import cli
    # cli modules
    cli.minimal()
    cli.graph()
    cli.handler()
    cli.misc()

    options = cli.parser.parse_args()
    if options.ignore_first:
        options.ignore = re.compile('.*_1.csv')

    # pre-processing
    csvs = utils.walk(options.csvs, options.ignore)
    groups = processing.group(csvs)
    dfs = processing.parse(groups)
    diffs = (processing.diff(m, f) for m, f in dfs)
    print(":: dynamic evaluating experiments")

    # types of process
    cli = (diffs, len(groups), options.long)
    if options.count_clusters:  # clustering
        print(":: load csv -> differentiating -> count short/mid/long")
        output_dataframe = processing.count_clusters(*cli)
    else:  # just getting the longs
        print(":: load csv -> differentiating -> mean -> tagging longs")
        processed = processing.mean(*cli)
        print(":: counting longs ")
        processed.long = processing.classify_longs(processed, options.long)
        output_dataframe = processing.count_longs(processed, options.interval)

    basename = utils.get_firstname(csvs[0])
    graph.plot_save(output_dataframe, basename, options)
    utils.save_csv(output_dataframe, basename, options)

if __name__ == '__main__':
    main()
