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
    Normalization modules to cleaning data

    * mar.processing.normalization.remove_nil
    * mar.processing.normalization.remove_zeros
    * mar.processing.normalization.normalize

"""


def remove_nil(df):
    if '(nil)' in df.index:
        return df.drop('(nil)')
    return df


def remove_zeros(malloc, column='req'):
    for index in malloc.index:
        if int(malloc.loc[index][column]) == 0:
            malloc.drop(index)
    return malloc


def normalize(df, nil=False):
    if not nil:
        df = remove_nil(df)
    reusage = df.groupby(level=0).cumcount()
    df.index = df.index.map(str) + reusage.map(lambda x: '-' + str(x))
    df.reset_index()
    return df
