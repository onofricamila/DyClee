#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from utils.micro_clusters.CF import CF
from utils.micro_clusters.bounding_box import BoundingBox
import numpy as np


class MicroCluster:
    
    def __init__(self, relativeSize, currTimestamp, point):
        self.relativeSize = relativeSize
        self.currTimestamp = currTimestamp # object
        self.boundingBoxesList = self.initBoundingBoxesList(point)
        self.hyperboxSizePerFeature = self.getHyperboxSizePerFeature()
        self.CF = self.initializeCF(point)
        self.label = -1 #"unclass"
        self.previousState = []
    


    def __repr__(self):
        return 'Micro Cluster'



    # initializes CF  
    def initializeCF(self, point):  
       # we assume point is a list of features
       LS = point
       # this vector will only have point elements squared
       SS = [a*b for a,b in zip(point, point)]
       now = self.currTimestamp.timestamp
       D = self._calculateD()
       # CF creation
       cf = CF(n=1, LS=LS, SS=SS, tl=now, ts=now, D=D)
       return cf
    
    
    
    # initializes boundingBox with point values 
    def initBoundingBoxesList(self, point):
        boundingBoxesList = []
        for i in range(len(point)):
            boundingBox = BoundingBox(minimun=-2 , maximun=2)
            boundingBoxesList.append(boundingBox)
        return boundingBoxesList
    
    
    
    # returns a list containing the size per feature. Indexes match those from point
    def getHyperboxSizePerFeature(self):
        hyperboxSizePerFeature = []
        for bb in self.boundingBoxesList:
            aux = bb.maximun - bb.minimun
            hyperboxSizePerFeature.append(self.relativeSize * abs(aux))
        return hyperboxSizePerFeature
    
    
    
    # retunrs true if the uc is reachable from a given element
    def isReachableFrom(self, point):
        myCentroid = self.getCentroid()
        maxDiff = float("-inf")
        featureIndex = 0
        # for each feature
        for i in range(len(point)):
            # difference between the element feature and the cluster centroid for that feature
            diff = abs(point[i] - myCentroid[i])
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
    def addElement(self, lambd, point=None):
        dt = self.currTimestamp.timestamp - self.CF.tl + 10
        decayComponent = 2 ** (-lambd * dt)
        self.updateTl()
        self.updateN(point, decayComponent)
        self.updateLS(point, decayComponent)
        self.updateSS(point, decayComponent)
#        # needs to check if bounding boxes change and recalculate hyperbox size
#        self.updateBoundingBoxesList(point)
#        self.updateHyperboxSizePerFeature()
        # then update u cluster density
        self.updateD()
        
        
        
    def updateTl(self):
        self.CF.tl = self.currTimestamp.timestamp
        
        
        
    def updateN(self, point, decayComponent):
        N = self.CF.n * decayComponent
        if point is not None:
            N += 1
        self.CF.n = N

        
    
    def updateLS(self, point, decayComponent):
        # forget
        for i in range(len(self.CF.LS)):
            self.CF.LS[i] = self.CF.LS[i] * decayComponent
        # add element
        if point is not None:
            for i in range(len(point)):
                self.CF.LS[i] = self.CF.LS[i] + point[i]
            
            
    
    def updateSS(self, point, decayComponent):
        # forget
        for i in range(len(self.CF.SS)):
            self.CF.SS[i] = self.CF.SS[i] * decayComponent
        # add element
        if point is not None:
            for i in range(len(point)):
                self.CF.SS[i] = self.CF.SS[i] + (point[i] **2)
        
    

    def updateBoundingBoxesList(self, point):
        for i in range(len(point)):
            mini = min(point[i], self.boundingBoxesList[i].minimun)
            maxi = max(point[i], self.boundingBoxesList[i].maximun)
            boundingBox = BoundingBox(minimun=mini , maximun=maxi)
            self.boundingBoxesList[i] = boundingBox

        
        
    def updateHyperboxSizePerFeature(self):
        self.hyperboxSizePerFeature = self.getHyperboxSizePerFeature()
        
        
        
    def updateD(self):
      self.CF.D = self._calculateD(n = self.CF.n)
    
    
      
    def _calculateD(self, n=1):
      V = np.prod(self.hyperboxSizePerFeature)
      return n / V
        
        
      
    def hasUnclassLabel(self):
      return (self.label is -1)
    
    
    
    def limit(self, i):
      return self.hyperboxSizePerFeature[i] /2
    
    
    
    # retunrs true if the microCluster is directly connected to another microCluster
    def isDirectlyConnectedWith(self, microCluster, uncommonDimensions):
      featuresCount = len(self.CF.LS)
      currentUncommonDimensions = 0
      myCentroid = self.getCentroid()
      microClusterCentroid = microCluster.getCentroid()
      # for each feature
      for i in range(featuresCount):
          # difference between the u cluster centroids for that feature
          aux = abs(myCentroid[i] - microClusterCentroid[i])
          # if for a given feature the element doesn't match the cluster, return false
          limit = self.limit(i)
          if aux >= (limit*2):
              currentUncommonDimensions += 1
      return currentUncommonDimensions <= uncommonDimensions
        
        
    def applyDecayComponent(self, lambd):
        self.addElement(lambd=lambd)
        
        
        
        
        
        
        
        
        
        
        
        
        