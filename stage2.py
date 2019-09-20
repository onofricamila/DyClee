#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:52:46 2019

@author: camila
"""
import numpy as np
import matplotlib.pyplot as plt

class Stage2:
  
  def __init__(self, s1ToS2ComQueue, s2ToS1ComQueue, dataContext, uncommonDimensions = 0):
        # communication instance variables    
        self.s1ToS2ComQueue = s1ToS2ComQueue
        self.s2ToS1ComQueue = s2ToS1ComQueue
        
        # stage2 algo instance variables
        self.dataContext = dataContext
        self.currentClusterId = 0
        self.mean = 0
        self.median = 0
        self.uncommonDimensions = uncommonDimensions
        
        
  def start(self):
    print("S2 start")
    while True:
      # wait for lists from s1
      msg = self.s1ToS2ComQueue.get()
      if msg == "DONE":
        break
      # uC lists were received 
      lists = msg
      print("s2 received lists: ", lists)
      # update mean and median
      self.updateMeanAndMedian(lists)
      print("S2 mean: ", self.mean)
      print("S2 median: ", self.median)
      # update lists
      updatedLists = self.updateLists(lists)
      print("S2 updatedLists: ", updatedLists)
      # send updated uCs lists to s1
      self.s2ToS1ComQueue.put(updatedLists)
      # form clusters
      self.formClusters(updatedLists)



  def updateLists(self, lists):
    print("S2 updateLists")
    aList, oList = lists
    
    print("S2 updateLists original aList: ", aList)
    print("S2 updateLists original oList: ", oList)

    newAList = []
    newOList = []
    
    for uC in aList:
      print("S2 updateLists aList: uC", uC)
      if self.isOutlier(uC):
        print("S2 updateLists aList: uC debe ir a oList")
        newOList.append(uC)
        
    for uC in oList:
      print("S2 updateLists oList: uC", uC)
      if self.isDense(uC) or self.isSemiDense(uC):
        print("S2 updateLists oList: uC debe ir a aList")
        newAList.append(uC)
        
    return (newAList, newOList)
        


  def updateMeanAndMedian(self, lists):
    aList, oList = lists
    concatenatedLists = aList + oList
    self.mean = self.calculateMeanFor(concatenatedLists)
    self.median = self.calculateMedianFor(concatenatedLists)     
    
  
  
  def formClusters(self, updatedLists):
    # reset currentClusterId
    self.currentClusterId = 0
    # extract lists
    updatedAList, updatedOList = updatedLists
    print("s2 formClusters")
    # join lists to get all the u clusters together
    uCs = updatedAList + updatedOList
    
    # it's unnecessary to look for dense uCs in the oList
    DMC = self.findDenseUcs(updatedAList)
    print("s2 formClusters DMC", DMC)
    alreadySeen = []
    
    for denseUc in DMC:
      if self.hasntBeenSeen(denseUc, alreadySeen):
        alreadySeen.append(denseUc)
        if denseUc.hasUnclassLabel():
          self.currentClusterId += 1
          denseUc.label = self.currentClusterId
          
        connectedUcs = self.findDirectlyConnectedUcsFor(denseUc, uCs)
        
        i = 0
        while i < len(connectedUcs):  
          conUc = connectedUcs[i]
          if self.isDense(conUc):
            conUc.label = self.currentClusterId
            alreadySeen.append(conUc)
            newConnectedUcs = self.findDirectlyConnectedUcsFor(conUc, uCs)
          
            for newNeighbour in newConnectedUcs:
              if self.hasntBeenSeen(newNeighbour, alreadySeen):
                if self.isDense(newNeighbour):
                  connectedUcs.append(newNeighbour)
              
                newNeighbour.label = self.currentClusterId
            
          i += 1
        
    # for loop finished -> clusters were formed 
    self.plotClusters(uCs)
    
    
        
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
    
     

  def findDirectlyConnectedUcsFor(self, uC, uCs):
    res = []
    for u in uCs:
      if uC.isDirectlyConnectedWith(u, self.uncommonDimensions):
        res.append(u)
    return res
  
  
          
  # plots current clusters          
  def plotClusters(self, uCs):
    # check if clusters are plottable
    print("S2 plotclusters uCs", uCs)
    firstEl = uCs[0]
    if len(firstEl.CF.LS) != 2:
      print("UNABLE TO DRAW CLUSTERS: IT'S NOT A 2D DATASET")
      return
    
    # let's plot!
    
    # first get a list with u cluster labels
    labelsPerUCluster = [uC.label for uC in uCs]
    # clusters will be a sequence of numbers (cluster number or -1) for each point in the dataset
    clusters = np.array(labelsPerUCluster)
    print("S2 plotclusters uCs CLUSTERS: ", clusters)
    
    # get uCs centroids
    centroids = [uC.getCentroid() for uC in uCs]
    
    # scatter needs 2 params: xs n ys (all values for dimension1 and all for d2);
    # 2 separate lists with those values, considering same index = same element values 
    # 1° extract centroids from centroids list
    # 2° generate an iterator with 2 elements: a list of xs and a list of ys
    # 3° get both lists
    
    # same as: 
    # x,y = zip(*centroids) plus plt.scatter(x, y)
    x,y = zip(*centroids)
    print("S2 plotclusters uCs x: ", x)
    print("S2 plotclusters uCs y: ", y)
    plt.scatter(x,y, c=clusters, cmap="nipy_spectral", marker="s", s=100)
    
    # set axes limits
    unitX = ( self.dataContext[0][1] - self.dataContext[0][0] ) * 10/100
    minAndMaxX = [self.dataContext[0][0] - unitX, self.dataContext[0][1] + unitX] 
    
    unitY = ( self.dataContext[1][1] - self.dataContext[1][0] ) * 10/100
    minAndMaxY = [self.dataContext[1][0] - unitX, self.dataContext[1][1] + unitY] 
    
    axes = plt.gca()
    axes.set_xlim(minAndMaxX)
    axes.set_ylim(minAndMaxY)
   
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.grid(color='k', linestyle=':', linewidth=1)
    plt.show()
      