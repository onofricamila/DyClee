#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from utils.uClusters.CF import CF
from utils.uClusters.boundingBox import BoundingBox
import numpy as np


class uCluster:
    
    def __init__(self, relativeSize, d):
        self.relativeSize = relativeSize
        self.boundingBoxesList = self.initBoundingBoxesList(d)
        self.hyperboxSizePerFeature = self.getHyperboxSizePerFeature()
        self.CF = self.initializeCF(d)
        self.label = -1 #"unclass"
        self.centroid = self.getCentroid()
        self.inmediatePreviousState = []
    
    
    def __repr__(self):
        return 'uCluster'



    # initializes CF  
    def initializeCF(self, d):  
       # we assume d is a list of features
       LS = d
       # this vector will only have d elements squared
       SS = [a*b for a,b in zip(d, d)]
       currentTime = datetime.datetime.now().time()
       D = self.getD()
       # CF creation
       cf = CF(n=1, LS=LS, SS=SS, tl=currentTime, ts=currentTime, D=D)
       return cf
    
    
    
    # initializes boundingBox with d values 
    def initBoundingBoxesList(self, d):
        boundingBoxesList = []
        for i in range(len(d)):
            boundingBox = BoundingBox(minimun=-2 , maximun=2)
            boundingBoxesList.append(boundingBox)
        return boundingBoxesList
    
    
    
    # returns a list containing the size per feature. Indexes match those from d
    def getHyperboxSizePerFeature(self):
        hyperboxSizePerFeature = []
        for bb in self.boundingBoxesList:
            aux = bb.maximun - bb.minimun
            hyperboxSizePerFeature.append(self.relativeSize * abs(aux))
        return hyperboxSizePerFeature
    
    
    
    # retunrs true if the uc is reachable from a given element
    def isReachableFrom(self, d):
        myCentroid = self.getCentroid()
        maxDiff = float("-inf")
        featureIndex = 0
        # for each feature
        for i in range(len(d)):
            # difference between the element feature and the cluster centroid for that feature
            diff = abs(d[i] - myCentroid[i])
            if diff > maxDiff:
              maxDiff = diff
              featureIndex = i
        # if for the max diff feature the element doesn't match the cluster, return false
        if maxDiff >= (self.limit(featureIndex)):
            return False
        # the element fits the u cluster
        return True
        
        
    
    # returns the u cluster centroid
    def getCentroid(self):
        centroid = []
        # for each feature
        for i in range(len(self.CF.LS)):
          centroid.append(self.CF.LS[i] / self.CF.n)
        return centroid
    
    
    
    # includes an element into the u cluster
    # updates CF vector
    def addElement(self, d):
        self.updateTl()
        self.updateN()
        self.updateLS(d)
        self.updateSS(d)
        self.updateCentroid()
#        # needs to check if bounding boxes change and recalculate hyperbox size
#        self.updateBoundingBoxesList(d)
#        self.updateHyperboxSizePerFeature()
        # then update u cluster density
        self.updateD()
        
        
        
    def updateTl(self):
        currentTime = datetime.datetime.now().time()
        self.CF.tl = currentTime
        
        
        
    def updateN(self):
        self.CF.n += 1
        
        
    
    def updateLS(self, d):
        for i in range(len(d)):
            self.CF.LS[i] = self.CF.LS[i] + d[i]  
            
            
    
    def updateSS(self, d):
        for i in range(len(d)):
            self.CF.SS[i] = self.CF.SS[i] + (d[i] **2)
        
    

    def updateCentroid(self):
      self.centroid = self.getCentroid()
      
      
        
    def updateBoundingBoxesList(self, d):
        for i in range(len(d)):
            mini = min(d[i], self.boundingBoxesList[i].minimun)
            maxi = max(d[i], self.boundingBoxesList[i].maximun)
            boundingBox = BoundingBox(minimun=mini , maximun=maxi)
            self.boundingBoxesList[i] = boundingBox

        
        
    def updateHyperboxSizePerFeature(self):
        self.hyperboxSizePerFeature = self.getHyperboxSizePerFeature()
        
        
        
    def updateD(self):
      self.CF.D = self.getD(n = self.CF.n)
    
    
      
    def getD(self, n=1): 
      V = np.prod(self.hyperboxSizePerFeature)
      return n / V
        
        
      
    def hasUnclassLabel(self):
      return (self.label is -1)
    
    
    
    def limit(self, i):
      return self.hyperboxSizePerFeature[i] /2
    
    
    
    # retunrs true if the uC is directly connected to another uC
    def isDirectlyConnectedWith(self, uC, uncommonDimensions):
      featuresCount = len(self.CF.LS)
      currentUncommonDimensions = 0
      myCentroid = self.getCentroid()
      uCCentroid = uC.getCentroid()
      # for each feature
      for i in range(featuresCount):
          # difference between the u cluster centroids for that feature
          aux = abs(myCentroid[i] - uCCentroid[i])
          # if for a given feature the element doesn't match the cluster, return false
          limit = self.limit(i)
          if aux >= (limit*2):
              currentUncommonDimensions += 1
      return currentUncommonDimensions <= uncommonDimensions
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        