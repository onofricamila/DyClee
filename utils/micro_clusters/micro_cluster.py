#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from utils.helpers.custom_math_fxs import manhattanDistance
from utils.micro_clusters.CF import CF
import numpy as np


class MicroCluster:
    
    def __init__(self, hyperboxSizePerFeature, currTimestamp, point):
        self.currTimestamp = currTimestamp # timestamp object
        self.hyperboxSizePerFeature = hyperboxSizePerFeature
        self.CF = self.initializeCF(point)
        self.label = -1 #"unclass"
        self.previousCentroid = []
    


    def __repr__(self):
        return 'Micro Cluster'



    # initializes CF  
    def initializeCF(self, point):  
       # we assume point is a list of features
       LS = point
       # this vector will only have point elements squared
       SS = [a*b for a,b in zip(point, point)]
       now = self.currTimestamp.timestamp
       # CF creation
       cf = CF(n=1, LS=LS, SS=SS, tl=now, ts=now)
       return cf


    
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
        if maxDiff >= (self.hyperboxSizePerFeature[i] / 2):
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
    def addElement(self, point, lambd):
        decayComponent = self.decayComponent(lambd)
        self.updateN(decayComponent, point)
        self.updateLS(decayComponent, point)
        self.updateSS(decayComponent, point)
        self.updateTl()



    def decayComponent(self, lambd):
        dt = self.currTimestamp.timestamp - self.CF.tl
        return 2 ** (-lambd * dt)


        
    def updateTl(self):
        self.CF.tl = self.currTimestamp.timestamp
        
        
        
    def updateN(self, decayComponent, point=None):
        N = self.CF.n * decayComponent
        if point is not None:
            N += 1
        self.CF.n = N

        
    
    def updateLS(self, decayComponent, point=None):
        # forget
        for i in range(len(self.CF.LS)):
            self.CF.LS[i] = self.CF.LS[i] * decayComponent
        # add element
        if point is not None:
            for i in range(len(point)):
                self.CF.LS[i] = self.CF.LS[i] + point[i]
            
            
    
    def updateSS(self, decayComponent, point=None):
        # forget
        for i in range(len(self.CF.SS)):
            self.CF.SS[i] = self.CF.SS[i] * decayComponent
        # add element
        if point is not None:
            for i in range(len(point)):
                self.CF.SS[i] = self.CF.SS[i] + (point[i] **2)

        

    def getD(self):
      V = np.prod(self.hyperboxSizePerFeature)
      return self.CF.n / V

    

    def hasUnclassLabel(self):
      return (self.label is -1)
    

    
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
          if aux >= self.hyperboxSizePerFeature[i]:
              currentUncommonDimensions += 1
      return currentUncommonDimensions <= uncommonDimensions
        


    def applyDecayComponent(self, lambd):
        decayComponent = self.decayComponent(lambd)
        self.updateN(decayComponent)
        self.updateLS(decayComponent)
        self.updateSS(decayComponent)
        


    def distanceTo(self, microCluster):
        return manhattanDistance(self.getCentroid(), microCluster.getCentroid())


        
        
        
        
        
        
        
        
        
        