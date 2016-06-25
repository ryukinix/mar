#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright © Manoel Vilela
#
#    @project: Memory Analysis Report
#     @author: Manoel Vilela
#      @email: manoel_vilela@engineer.com
#

from os import getcwd

__version__ = '0.5'
__author__ = 'Manoel Vilela'
__email__ = 'manoel_vilela@engineer.com'
__url__ = 'https://gitlab.com/ryukinix/mar'

# constants
NANOSECOND = 1e9
CURRENT_DIRECTORY = getcwd()
MATCHING_PATTERNS = ('free', 'malloc')
