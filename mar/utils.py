#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright © Manoel Vilela
#
#    @project: Memory Analysis Report
#     @author: Manoel Vilela
#      @email: manoel_vilela@engineer.com
#


import os


def get_firstname(first, suffix='report'):
    string = ''
    if '_' in first:
        string += first.split('_')[0]
    elif '-' in first:
        string += first.split('-')[0]

    tokens = [string or first, suffix]

    return '-'.join(filter(bool, tokens))


def get_name(path):
    return get_firstname(os.path.basename(path), suffix='')
