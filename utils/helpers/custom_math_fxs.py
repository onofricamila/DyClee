#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def _ss(data, mean):
    """Return sum of square deviations of sequence data."""
    ss = sum((x-mean)**2 for x in data)
    return ss


def stddev(data, mean, ddof=0):
    """Calculates the population standard deviation
    by default; specify ddof=1 to compute the sample
    standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data, mean)
    pvar = ss/(n-ddof)
    return pvar**0.5


# returns the manhattan distance between a and b
def manhattanDistance(a, b):
    dist = 0
    # for every feature/dimension
    for i in range(len(a)):
        diff = a[i] - b[i]
        dist = dist + abs(diff)
    return dist



