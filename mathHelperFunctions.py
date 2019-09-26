#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 12:30:17 2019

@author: camila
"""

# helper functions
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
