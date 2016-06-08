#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#


from argparse import ArgumentParser
from mar.interval import Interval
import fnmatch
import re

parser = ArgumentParser()
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
    help="Show the "

)

# the target path to save the report
parser.add_argument(
    '-t', '--target',
    dest='target',
    default='memory-analysis-report',
    help="The path (can be a folder name or path) to save the output"
)

# the long range
parser.add_argument(
    '-l', '--long-range',
    dest='long',
    default=Interval('[1, 3]'),
    type=Interval,
    help=("The long range range like [x, y] (closed-range) to labelize the allocation time.\n"
          "Use +inf or -inf to handle infinite intervals like [-inf, +inf] will get all allocations")
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
    help="The list of pair malloc_0x.csv free_0x separated by spaces or a dir",
    nargs='+'
)

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
