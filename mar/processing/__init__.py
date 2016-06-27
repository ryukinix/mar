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
    This module is the main module of all project, whose
    is reliable to do all the processing data using Pandas.

    * mar.processing.actions:
        * mar.processing.actions.diff
        * mar.processing.actions.merge
        * mar.processing.actions.mean
    * mar.processing.classify:
        * mar.processing.classify.clusters
        * mar.processing.classify.tag
        * mar.processing.classify.longs
    * mar.processing.count:
        * mar.processing.count.longs
        * mar.processing.count.clusters
    * mar.processing.normalization:
        * mar.processing.normalization.remove_nil
        * mar.processing.normalization.remove_zeros
        * mar.processing.normalization.normalize
    * mar.processing.io:
        * mar.processing.io.read_malloc
        * mar.processing.io.read_free
        * mar.processing.io.parse
        * mar.processing.io.group
        * mar.processing.io.load
        * mar.processing.io.save
"""

from . import actions
from . import classify
from . import count
from . import io
from . import normalization

__all__ = [
    'actions',
    'classify',
    'count',
    'io',
    'normalization'
]
