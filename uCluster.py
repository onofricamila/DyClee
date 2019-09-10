#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:19:40 2019

@author: camila
"""
import datetime

class uCluster:
    
    
    
    def __init__(self, relativeSize, d):
        self.relativeSize = relativeSize
        self.CF = self.initializeCF(d)
        
        
        
    # initializes CF  
    def initializeCF(self, d):  
        CF = dict()  
        
        # number of elements
        CF["n"] = 1
        
        # we assume d is a list of features
        CF["LS"] = d
        
        # TODO check calculation of SS 
        CF["SS"] = [a*b for a,b in zip(d, d)]
        
        currentTime = datetime.datetime.now().time()
        CF["tl"] = currentTime
        CF["ts"] = currentTime
        
        CF["D"] = 0
        
        # no puse la clase ... 
        
        return CF
    
    
    
        