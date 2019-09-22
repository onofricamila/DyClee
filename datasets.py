#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 20:03:56 2019

@author: camila
"""

# pilot 
pilot = [[2, 10]]

# test forming 2 uCs
forming2uCs = [[2, 10], [80, 100]]

# test adding element to uC (notice change in D)
addingElToUc = [[2, 10], [1, 9]]

# test choosing closest reachable uC
choosingClosestReachableUc = [[2, 10], [11, 19], [7, 15]]

# test going from uC to noise
fromUcToNoise = [[2, 10], [80, 100], [1, 9]]

# test going from uC to noise with more data
fromUcToNoiseV2 = [[2, 10], [1, 9], [80, 100], [83, 98], [5, 13]]

# test forming many uCs
formingManyUcs = [[2, 10], [30, 40], [1, 9], [80, 100]]


# min and max for each feature
dataContext = [[0, 100], [0, 100]]