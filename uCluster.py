#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:19:40 2019

@author: camila
"""
import datetime
from CF import CF

class uCluster:
    
    
    
    def __init__(self, relativeSize, d):
        self.relativeSize = relativeSize
        self.CF = self.initializeCF(d)
        self.boundingBox = self.initBoundingBox(d)
        
        
        
    # initializes CF  
    def initializeCF(self, d):  
       # we assume d is a list of features
       LS = d
       
       # TODO check calculation of SS 
       SS = [a*b for a,b in zip(d, d)]
        
       currentTime = datetime.datetime.now().time()
        
       # CF creation
       cf = CF(n=1, LS=LS, SS=SS, tl=currentTime, ts=currentTime, D=0)
             
       return cf
    
    
    
    # initializes boundingBox with d values  
    def initBoundingBox(self, d):
        boundingBox = []
        
        for f in d:
            res = dict()
            res['min'] = f
            res['max'] = f
            boundingBox.append(res)
        
        return boundingBox
    
    
    
    # returns a list containing the size per feature. Indexes match those from d
    def hyperboxSizePerFeature(self):
        hyperboxSizePerFeature = []
        
        for b in self.boundingBox:
            maxi = b.get('max')
            mini = b.get('min')
            hyperboxSizePerFeature.append(self.relativeSize * abs(maxi - mini))
        
        return hyperboxSizePerFeature
    
    
    
    # checks if the uc is reachable from a given element
    def isReachableFrom(self, d):
        return lala
        
    
        
    def getCentroid(self):
        return self.CF.LS / self.CF.n
        