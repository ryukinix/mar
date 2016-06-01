#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

import os


def get_firstname(first):
    string = ''
    if '_' in first:
        string += first.split('_')[0]
    elif '-' in first:
        string += first.split('-')[0]

    return string + 'report'


def get_name(path):
    return get_firstname(os.path.basename(path))
