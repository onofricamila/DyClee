#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:52:46 2019

@author: camila
"""
import numpy as np

# TODO plot obtained clusters
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
      # send updated uCs lists to s1
      self.s2ToS1ComQueue.put(updatedLists)
      # form clusters
      # it's unnecessary to look for dense uCs in the oList
      updatedAList, updatedOList = updatedLists
      self.formClusters(updatedAList)



  def updateLists(self, lists):
    aList, oList = lists
    
    newAList = aList
    newOList = oList
    
    self.mean = self.calculateMeanFor(aList + oList)
    self.median = self.calculateMedianFor(aList + oList)
    
    for uC in aList:
      if self.isOutlier(uC):
        newAList.remove(uC)
        newOList.append(uC)
        
    for uC in oList:
      if self.isDense(uC) or self.isSemiDense(uC):
        newAList.append(uC)
        newOList.remove(uC)
        
    
  
  def formClusters(self, uCs):
    DMC = self.findDenseUcs(uCs)
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
        
        
        
  def calculateMeanFor(self, uCs):   
     return  np.mean([c.CF.D for c in uCs])
     
   
    
  def calculateMedianFor(self, uCs):   
     return  np.median([c.CF.D for c in uCs])
   
          
        
  # returns true if a given u cluster is considered dense
  def isDense(self, uC):   
     return (uC >= self.mean and uC >= self.median)
     
   
  
  # returns true if a given u cluster is considered semi dense
  def isSemiDense(self, uC):   
     # xor
     return (uC >= self.mean) != (uC >= self.median)
   
    
    
  # returns true if a given u cluster is considered outlier
  def isOutlier(self, uC):   
     return (uC < self.mean and uC < self.median) 
  
  
  
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
      