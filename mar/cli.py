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
    Handle all the Command Line Interface

    We have three principal modules:

    * mar.cli.minimal:
        csvs (positional)
        --interval
        --target

    * mar.cli.misc:
        --verbose
        --ignore
        --ignore-first
        --version

    * mar.cli.graph:
        --show-graph
        --save-graph

    * mar.cli.handler:
        --count-clusters
        --long-range

"""


from argparse import ArgumentParser
from mar.interval import Interval
import fnmatch
import re
import mar

parser = ArgumentParser(description=mar.__abstract__)


def minimal():
    # the target path to save the report
    parser.add_argument(
        '-t', '--target',
        dest='target',
        default='.',
        help="The path (can be a folder name or path) to save the output"
    )

    # the slice to control the how long is counted
    parser.add_argument(
        "-i", "--interval",
        dest='interval',
        default=1000,
        type=int,
        help="The interval number to count longs on streaking rows"
    )

    # the default argument evaluation handled about the csv files
    # or directories
    parser.add_argument(
        "csvs",
        help=("The list of pair malloc_0x.csv "
              "free_0x separated by spaces or a dir"),
        nargs='+'
    )


def misc():
    parser.add_argument(
        '-v', '--verbose',
        dest='verbose',
        default=False,
        action='store_true',
        help="Allow the user control printint or not control operations",
    )

    parser.add_argument(
        '--ignore',
        dest='ignore',
        default='',
        type=lambda x: re.compile(fnmatch.translate(x)),
        help='Pass a wildcard pattern to file experiments on reading',
    )

    parser.add_argument(
        '--ignore-first',
        dest='ignore_first',
        default=False,
        action='store_true',
        help='Ignore the first experiment (the same of --ignore *1.csv)',
    )

    parser.add_argument(
        '-V', '--version',
        default=False,
        help='Print the version of MAR.'
    )


def graph():
    # active the graph print
    parser.add_argument(
        "--show-graph",
        dest='show_graph',
        default=False,
        action='store_true',
        help="Show the graph after pre-processing"
    )
    # save the graph on the end
    parser.add_argument(
        '--save-graph',
        dest='save_graph',
        default=False,
        action='store_true',
        help="Save the graph on target after pre-processing"
    )


def handler():
    parser.add_argument(
        '-c', '--count-clusters',
        dest='count_clusters',
        default=False,
        action='store_true',
        help="Count the short/mid/long allocations and save a csv."
    )

    # the long range
    parser.add_argument(
        '-l', '--long-range',
        dest='long',
        default=Interval('[1, 3]'),
        type=Interval,
        help=("The long range range like [x, y] (closed-range) or "
              "(a, b) (open-range) to labelize the allocation time.\n"
              "Use +inf or -inf to handle infinite intervals "
              "like (-inf, +inf) will get all allocations"),
    )
