#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:19:40 2019

@author: camila
"""
import datetime
from CF import CF
from boundingBox import BoundingBox


class uCluster:
    
    
    
    def __init__(self, relativeSize, d):
        self.relativeSize = relativeSize
        self.CF = self.initializeCF(d)
        self.boundingBoxesList = self.initBoundingBoxesList(d)
        
        
        
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
    def initBoundingBoxesList(self, d):
        boundingBoxesList = []
        
        for f in d:
            boundingBox = BoundingBox(minimun=f , maximun=f)
            boundingBoxesList.append(boundingBox)
        
        return boundingBoxesList
    
    
    
    # returns a list containing the size per feature. Indexes match those from d
    def hyperboxSizePerFeature(self):
        hyperboxSizePerFeature = []
        
        for bb in self.boundingBoxesList:
            aux = bb.maximun - bb.minimun
            hyperboxSizePerFeature.append(self.relativeSize * abs(aux))
        
        return hyperboxSizePerFeature
    
    
    
    # checks if the uc is reachable from a given element
    def isReachableFrom(self, d):
        return ""
        
    
        
    def getCentroid(self):
        return self.CF.LS / self.CF.n
        