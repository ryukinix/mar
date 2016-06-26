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

# information about the project
__version__ = '0.5.1'
__date__ = '2016'
__author__ = 'Manoel Vilela'
__email__ = 'manoel_vilela@engineer.com'
__url__ = 'https://gitlab.com/ryukinix/mar'
__abstract__ = (
    'Read malloc-free pairs CSVs from debugmalloc program,'
    'do a sequence of stats processing to processing data.'
    'On the final of processing, get a summarization and put on new CSV.'
    'Beyond that,  the user can choice by CLI to save or show graphs. '
    'v{} Developed by Manoel Vilela on Federal University of Pará'
    'as Student Researcher at {}'.format(__version__, __date__))

# constants
NANOSECOND = 1e9
CURRENT_DIRECTORY = getcwd()
MATCHING_PATTERNS = ('free', 'malloc')
