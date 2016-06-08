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

    def __repr__(self):
        return '<{cls} {interval} at {id}>'.format(cls=self.__name__(),
                                                   interval=self.interval,
                                                   id=hex(id(self)))

    def __str__(self):
        return self.interval

    def parse(self, interval):
        return list(map(float, 
                        interval.strip('[]()').split(',')))

    def __contains__(self, element):
        return self >= element and self <= element

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