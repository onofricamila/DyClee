#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:52:46 2019

@author: camila
"""
import numpy as np
import matplotlib.pyplot as plt

class Stage2:
  
  def __init__(self, s1ToS2ComQueue, s2ToS1ComQueue, uncommonDimensions = 0):
        # communication instance variables    
        self.s1ToS2ComQueue = s1ToS2ComQueue
        self.s2ToS1ComQueue = s2ToS1ComQueue
        
        # stage2 algo instance variables
        self.currentClusterId = 1
        self.mean = 0
        self.median = 0
        self.uncommonDimensions = uncommonDimensions
        
        
        
  def start(self):
    while True:
      # wait for lists from s1
      lists = self.s1ToS2ComQueue.get()
      updatedLists = self.updateLists(lists)
      self.updateMeanAndMedian()
      # send updated uCs lists to s1
      self.s2ToS1ComQueue.put(updatedLists)
      # update mean and median
      updatedAList, updatedOList = updatedLists
      self.updateMeanAndMedian(updatedAList + updatedOList)
      # form clusters
      self.formClusters(updatedLists)



  def updateLists(self, lists):
    aList, oList = lists
    
    self.updateMeanAndMedian(aList + oList)
    
    newAList = aList
    newOList = oList
    
    for uC in aList:
      if self.isOutlier(uC):
        newAList.remove(uC)
        newOList.append(uC)
        
    for uC in oList:
      if self.isDense(uC) or self.isSemiDense(uC):
        newAList.append(uC)
        newOList.remove(uC)
  


  def updateMeanAndMedian(self, concatenatedLists):
    self.mean = self.calculateMeanFor(concatenatedLists)
    self.median = self.calculateMedianFor(concatenatedLists)     
    
  
  
  def formClusters(self, updatedLists):
    updatedAList, updatedOList = updatedLists
      
    # it's unnecessary to look for dense uCs in the oList
    DMC = self.findDenseUcs(updatedAList)
    
    alreadySeen = []
    
    for denseUc in DMC:
      if self.hasntBeenSeen(denseUc, alreadySeen):
        alreadySeen.append(denseUc)
        if denseUc.hasUnclassLabel():
          denseUc.label = self.currentClusterId
          
        connectedUcs = self.findConnectedUcsFor(denseUc)
        
        i = 0
        while i < len(connectedUcs):  
          conUc = connectedUcs[i]
          if self.isDense(conUc):
            conUc.label = self.currentClusterId
            alreadySeen.append(conUc)
            newConnectedUcs = self.findConnectedUcsFor(conUc)
          
            for newNeighbour in newConnectedUcs:
              if self.isDense(newNeighbour):
                connectedUcs.append(newNeighbour)
              
              newNeighbour.label = self.currentClusterId
            
          i += 1
        
        self.currentClusterId += 1
        
    # for loop finished -> clusters were formed 
    self.plotClusters(updatedAList + updatedOList)
    
    
        
  def calculateMeanFor(self, uCs):   
     return  np.mean([uC.CF.D for uC in uCs])
     
   
    
  def calculateMedianFor(self, uCs):   
     return  np.median([uC.CF.D for uC in uCs])
   
          
        
  # returns true if a given u cluster is considered dense
  def isDense(self, uC):   
     return (uC.CF.D >= self.mean and uC.CF.D >= self.median)
     
   
  
  # returns true if a given u cluster is considered semi dense
  def isSemiDense(self, uC):   
     # xor
     return (uC.CF.D >= self.mean) != (uC.CF.D >= self.median)
   
    
    
  # returns true if a given u cluster is considered outlier
  def isOutlier(self, uC):   
     return (uC.CF.D < self.mean and uC.CF.D < self.median) 
  
  
  
  # returns only dense u clusters from a set of u clusters
  def findDenseUcs(self, uCs):
    res = []
    for uC in uCs:
      if self.isDense(uC):
        res.append(uC)
    return res
  
  
  
  def hasntBeenSeen(self, uC, alreadySeen):
    return (uC not in alreadySeen)
    
     
    
  def findConnectedUcsFor(self, uC, uCs):
    res = []
    self.auxFindConnectedUcsFor(uC, uCs, res)
    return res
  
  
  
  def auxFindConnectedUcsFor(self, uC, uCs, res):
    for x in uCs:
      if (uC.isDirectlyConnectedWith(x, self.uncommonDimensions)):
        if (x not in res):
          res.append(x)
          self.auxFindConnectedUcsFor(x, uCs, res)
          
          
          
  # plots current clusters          
  def plotClusters(self, uCs):
    # check if clusters are plottable
    firstEl = uCs[0]
    if len(firstEl.CF.Ls) != 0:
      print("UNABLE TO DRAW CLUSTERS: IT'S NOT A 2D DATASET")
      return
    
    # let's plot!
    
    # first get a list with u cluster labels
    labelsPerUCluster = [uc.label for uc in uCs]
    # clusters will be a sequence of numbers (cluster number or -1) for each point in the dataset
    clusters = np.array(labelsPerUCluster)
    
    # get uCs centroids
    centroids = [uc.getCentroid() for uc in uCs]
    
    # scatter needs 2 params: xs n ys (all values for dimension1 and all for d2);
    # 2 separate lists with those values, considering same index = same element values 
    # 1° extract centroids from centroids list
    # 2° generate an iterator with 2 elements: a list of xs and a list of ys
    # 3° get both lists
    
    # same as: 
    # x,y = zip(*centroids) plus plt.scatter(x, y)
    plt.scatter(*zip(*centroids), c=clusters, cmap="plasma")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.show()
      