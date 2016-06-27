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
    The main module of the core project of MAR.

    This module is used as the entry point of the python package.

    * mar.main.run
"""


import re

from mar import processing
from mar import graph
from mar import utils


def run():
    """Construct the CLI and do the main processing data for MAR"""
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
    groups = processing.io.group(csvs)
    dfs = processing.io.parse(groups)
    diffs = (processing.actions.diff(m, f) for m, f in dfs)
    print(":: dynamic evaluating experiments")

    if options.count_clusters:  # clustering
        print(":: load csv -> differentiating -> count short/mid/long")
        output_dataframe = processing.count.clusters(diffs, 
                                                     total=len(groups),
                                                     long_range=options.long)
    else:  # just getting the longs
        print(":: load csv -> differentiating -> mean -> tagging longs")
        processed = processing.actions.mean(diffs, total=len(groups))
        print(":: counting longs ")
        processed.long = processing.classify.longs(processed, options.long)
        output_dataframe = processing.count.longs(processed, options.interval)

    basename = utils.get_firstname(csvs[0], 'report')
    graph.plot_save(output_dataframe, basename, options)
    processing.io.save(output_dataframe, basename, options.verbose)

if __name__ == '__main__':
    run()
