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
        
        
        
  def start(self):
    while 1:
      # TODO wait till s1 sends uCs lists
      if self.listsReceivedFromS1():
        # TODO get s1 uCs lists
        lists = self.getUcsLists()
        updatedLists = self.updateLists(lists)
        # TODO send updated uCs lists to s1
        self.sendUpdatedListsToS1()
        self.formClusters(updatedLists)
    
    
  
  def formClusters(self, uCs):
    DMC = self.findDenseUcs(uCs)
    alreadySeen = []
    
    for denseUc in DMC:
      if self.hasntBeenSeen(denseUc, alreadySeen):
        alreadySeen.append(denseUc)
        if denseUc.isOutlier():
          denseUc.label = self.currentClusterId
          
        connectedUcs = self.findConnectedUcsFor(denseUc)
        
        i = 0
        while i < len(connectedUcs):  
          conUc = connectedUcs[i]
          if self.isDense(conUc, uCs):
            conUc.label = self.currentClusterId
            alreadySeen.append(conUc)
            conUcConnectedUcs = self.findConnectedUcsFor(conUc)
          
            for conUcConUc in conUcConnectedUcs:
              if self.isDense(conUcConUc):
                connectedUcs.append(conUcConUc)
              
              conUcConUc.label = self.currentClusterId
            
          i +=   1
        
        self.currentClusterId += 1
        
          
        
  # returns true if a given u cluster is considered dense
  def isDense(self, uC, uCs):   
     mean = np.mean([c.CF.D for c in uCs])
     median = np.median([c.CF.D for c in uCs])
     
     return (uC >= mean and uC >= median)
     
   
  
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
      