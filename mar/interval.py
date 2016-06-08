#!/usr/bin/env python
# coding=utf-8
#
#   Python Script
#
#   Copyright © Manoel Vilela
#
#

"""

    Basic handler of mathematical intervals like:
    [a, b], (x, y), [c, +inf[


"""

class Interval(object):

    def __init__(self, interval):
        self.interval = interval
        self.left, self.right = self.parse(self.interval)

    def parse(self, interval):
        return list(map(int, interval.strip('[]()').split(',')))

    def __contains__(self, element):
        return self > element and self < element

    def __gt__(self, element):
        return element > self.right

    def __lt__(self, element):
        return element < self.left

    def __ge__(self, element):
        return element <= self.right

    def __le__(self, element):
        return element >= self.right