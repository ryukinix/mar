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

    Basic handler of mathematical intervals like:
    [a, b], (x, y), [c, +inf[

"""

import numpy as np


class Interval(object):

    def __init__(self, interval):
        self.interval = str(interval).strip()
        self.left, self.right = self.parse(self.interval)
        self.lclosed, self.rclosed = self.infer_range()

    def __repr__(self):
        return '<{cls} {interval} at {id}>'.format(cls=self.__name__(),
                                                   interval=self.interval,
                                                   id=hex(id(self)))

    def infer_range(self):
        lclosed, rclosed = True, True
        if (self.interval.startswith('(') or
           (self.interval.startswith(']'))):
            lclosed = False
        if (self.interval.endswith(')') or
           (self.interval.startswith('['))):
            rclosed = False

        return lclosed, rclosed

    def __str__(self):
        return self.interval

    def parse(self, interval):
        return list(map(np.float,
                        interval.strip('[]()').split(',')))

    def __contains__(self, element):
        return (((self.rclosed and self >= element) or
                 (not self.rclosed and self > element)) and
                ((self.lclosed and self <= element) or
                 (not self.lclosed and self < element)))

    def __gt__(self, element):
        return self.right > element

    def __lt__(self, element):
        return self.left < element

    def __ge__(self, element):
        return self.right >= element

    def __le__(self, element):
        return self.left <= element

    @classmethod
    def __name__(cls):
        return cls.__name__
