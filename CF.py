#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 14:55:28 2019

@author: camila
"""

class CF:
    
    def __init__(self, n, LS, SS, tl, ts, D):
        # number of elements
        self.n = n
        # vector containing the linear sum of each feature over the n objects
        self.LS = LS
        # the square sum of features over the n objects
        self.SS = SS
        # time when the last object was assigned to the μ cluster
        self.tl = tl
        # time when the μ cluster was created
        self.ts = ts
        # the μ cluster density
        self.D = D