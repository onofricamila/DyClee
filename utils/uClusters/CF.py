#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
        
        
        
    def __repr__(self):
     return f'CF =>\n\t\tn: {self.n},\n\t\tLS: {self.LS},\n\t\tSS: {self.SS},\n\t\ttl: {self.tl},\n\t\tts: {self.ts},\n\t\tD: {self.D}'
        
        