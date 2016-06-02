#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#


from argparse import ArgumentParser

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

# the long size
parser.add_argument(
    '-l', '--long-size',
    dest='long',
    default=1,
    type=float,
    help="The long size in seconds to labelize the allocation time"
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
    type=str,
    help='Pass a regex pattern to file experiments on reading',
)


parser.add_argument(
    '--ignore-first',
    dest='ignore_first',
    default=False,
    action='store_true',
    help='Ignore the first experiment (the same of --ignore .*1.csv ',
)
