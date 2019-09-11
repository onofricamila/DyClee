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
        self.hyperboxSizePerFeature = self.getHyperboxSizePerFeature()
        
        
        
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
    def getHyperboxSizePerFeature(self):
        hyperboxSizePerFeature = []
        
        for bb in self.boundingBoxesList:
            aux = bb.maximun - bb.minimun
            hyperboxSizePerFeature.append(self.relativeSize * abs(aux))
        
        return hyperboxSizePerFeature
    
    
    
    # retunrs true (1) if the uc is reachable from a given element
    def isReachableFrom(self, d):
        # for each feature
        for i in range(len(d)):
            # difference between the element feature and the cluster centroid for that feature
            aux = abs(d[i] - self.getICentroid)
            # if for a given feature the element doesn't match the cluster, return false
            if aux >= (self.hyperboxSizePerFeature[i] / 2):
                return 0
        
        # the element fits the u cluster
        return 1
        
        
    
    # returns the u cluster centroid for a given feature considering the feature index
    def getICentroid(self, i):
        return self.CF.LS[i] / self.CF.n
    
    
    
    # includes an element into the u cluster
    # updates CF vector
    def addElement(self, d):
        
        
        
        
        
        
        
        
        
        