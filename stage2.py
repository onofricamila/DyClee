#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:52:46 2019

@author: camila
"""
import numpy as np

class Stage2:
  
  def __init__(self):
        self.currentClusterId = 1
        self.mean = 0
        self.median = 0
        
        
        
  def start(self):
    while 1:
      # TODO wait till s1 sends uCs lists
      if self.listsReceivedFromS1():
        # TODO get s1 uCs lists
        lists = self.getUcsLists()
        updatedLists = self.updateLists(lists)
        # TODO send updated uCs lists to s1
        self.sendUpdatedListsToS1()
        # it's unnecessary to look for dense uCs in the oList
        self.formClusters(updatedLists.get("aList"))



  def updateLists(self, lists):
    aList = lists.get("aList")
    oList = lists.get("oList")
    
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
            conUcConnectedUcs = self.findConnectedUcsFor(conUc)
          
            for conUcConUc in conUcConnectedUcs:
              if self.isDense(conUcConUc):
                connectedUcs.append(conUcConUc)
              
              conUcConUc.label = self.currentClusterId
            
          i +=   1
        
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
      if (uC.isDirectlyConnectedWith(x)):
        if (x not in res):
          res.append(x)
          self.auxFindConnectedUcsFor(x, uCs, res)
      