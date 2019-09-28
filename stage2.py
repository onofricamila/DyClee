#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:52:46 2019

@author: camila
"""
import numpy as np
import matplotlib.pyplot as plt
from customizedPrinting import printInMagentaForDebugging


class Stage2:
  
  def __init__(self, s1ToS2ComQueue, s2ToS1ComQueue, uncommonDimensions = 0):
        # communication instance variables    
        self.s1ToS2ComQueue = s1ToS2ComQueue
        self.s2ToS1ComQueue = s2ToS1ComQueue
        
        # stage2 algo instance variables
        self.densityMean = 0
        self.densityMedian = 0
        self.uncommonDimensions = uncommonDimensions
        
        
        
        
  def start(self):
    while True:
      # wait for lists from s1
      msg = self.s1ToS2ComQueue.get()
      if msg == "DONE":
        break
      # uC lists were received 
      lists = msg
      # update mean and median
      self.updateMeanAndMedian(lists)
      # update lists
      updatedLists = self.updateLists(lists)
      # send updated uCs lists to s1
      self.s2ToS1ComQueue.put(updatedLists)
      # form clusters
      self.formClusters(updatedLists)




  def updateLists(self, lists):
    aList, oList = lists
    
    newAList = []
    newOList = []
    
    concatenatedLists = aList + oList
    
    for uC in concatenatedLists:
      if self.isOutlier(uC):
        newOList.append(uC)
      else:
        # uC is dense or semi dense
        newAList.append(uC)
        
    return (newAList, newOList)
        



  def updateMeanAndMedian(self, lists):
    aList, oList = lists
    concatenatedLists = aList + oList
    self.densityMean = self.calculateMeanFor(concatenatedLists)
    self.densityMedian = self.calculateMedianFor(concatenatedLists)     
    
  
  
  
  def formClusters(self, updatedLists):
    # init currentClusterId
    currentClusterId = 0
    # extract lists
    updatedAList, updatedOList = updatedLists
    # reset uCs labels as -1
    self.resetLabelsAsUnclass(updatedAList)
    self.resetLabelsAsUnclass(updatedOList)
    # join lists to get all the u clusters together
    uCs = updatedAList + updatedOList
   
    # it's unnecessary to look for dense uCs in the oList
    DMC = self.findDenseUcs(updatedAList)
    alreadySeen = []
    
    for denseUc in DMC:
      if self.hasntBeenSeen(denseUc, alreadySeen):
        alreadySeen.append(denseUc)
        if denseUc.hasUnclassLabel():
          currentClusterId += 1
          denseUc.label = currentClusterId

        connectedUcs = self.findDirectlyConnectedUcsFor(denseUc, updatedAList)
        
        i = 0
        while i < len(connectedUcs):  
          conUc = connectedUcs[i]
          if self.isDense(conUc):
            conUc.label = currentClusterId
            alreadySeen.append(conUc)
            newConnectedUcs = self.findDirectlyConnectedUcsFor(conUc, updatedAList)
          
            for newNeighbour in newConnectedUcs:
              if self.hasntBeenSeen(newNeighbour, alreadySeen):
                if self.isDense(newNeighbour):
                  connectedUcs.append(newNeighbour)
              
                newNeighbour.label = currentClusterId
            
          i += 1
        
    # for loop finished -> clusters were formed 
    self.plotClusters(uCs)
    
    
    
        
  def resetLabelsAsUnclass(self, uCs):
    for uC in uCs:
      uC.label = -1
    
  
  
  
  def calculateMeanFor(self, uCs):   
     return  np.mean([uC.CF.D for uC in uCs])
     
   
   
    
  def calculateMedianFor(self, uCs):   
     return  np.median([uC.CF.D for uC in uCs])
   
          
        
  # returns true if a given u cluster is considered dense
  def isDense(self, uC):   
     return (uC.CF.D >= self.densityMean and uC.CF.D >= self.densityMedian)
     
   
  
  # returns true if a given u cluster is considered semi dense
  def isSemiDense(self, uC):   
     # xor
     return (uC.CF.D >= self.densityMean) != (uC.CF.D >= self.densityMedian)
   
    
    
  # returns true if a given u cluster is considered outlier
  def isOutlier(self, uC):   
     return (uC.CF.D < self.densityMean and uC.CF.D < self.densityMedian) 
  
  
  
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
    firstEl = uCs[0]
    if len(firstEl.CF.LS) != 2:
      print("UNABLE TO DRAW CLUSTERS: IT'S NOT A 2D DATASET")
      return
    
    # let's plot!
    
    # first get a list with u cluster labels
    labelsPerUCluster = [uC.label for uC in uCs]
    # clusters will be a sequence of numbers (cluster number or -1) for each point in the dataset
    clusters = np.array(labelsPerUCluster)
    printInMagentaForDebugging("S2 plotclusters uCs CLUSTERS: " + '\n' + clusters.__repr__() + '\n')
    
    # get uCs centroids
    centroids = [uC.getCentroid() for uC in uCs]
    
    x,y = zip(*centroids)
    printInMagentaForDebugging("S2 plotclusters uCs x: " + '\n' + x.__repr__() + '\n')
    printInMagentaForDebugging("S2 plotclusters uCs y: " + '\n' + y.__repr__())
    plt.scatter(x,y, c=clusters, cmap="nipy_spectral", marker="s")
    
    # set axes limits
    minAndMaxDeviations = [-2.2, 2.2]
    
    axes = plt.gca()
    axes.set_xlim(minAndMaxDeviations)
    axes.set_ylim(minAndMaxDeviations)
    
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.grid(color='k', linestyle=':', linewidth=1)
    plt.show()
      