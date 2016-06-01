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
    if '_' in first:
        return first.split('_')[0]
    elif '-' in first:
        return first.split('-')[0]
    else:
        return 'report'


def get_name(path):
    return get_firstname(os.path.basename(path))
