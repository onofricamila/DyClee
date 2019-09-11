#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:35:06 2019

@author: camila
"""

import numpy as np
from uCluster import uCluster

class Stage1:
    
    def __init__(self, relativeSize, tGlobal=1):
        self.relativeSize = relativeSize
        self.tGlobal = tGlobal        
        self.aList = []
        self.oList = []
    
    
    # main method
    def formUcs(self, dataset):
    # ASSUMPTIONS: dataset es un vector de vectores    
    
        processedElements = 0
        
        for d in dataset:
            # processed_elements ++
            processedElements += 1
            
            # TODO receive updated lists from stage 2 !!!!!!!!!!!!!!!!!!!!
            self.checkMsgFromStage2()
            
            # find reachable u clusters for the new element
            reachableUcs = self.findReachableUcs(d)
            
            if not reachableUcs:
                # empty list -> create u cluster from element 
                # the uC will have the parametrized relative size
                uC = uCluster(self, self.relativeSize, d)
                self.oList.append(uC) 
                
            else: 
                # find closest reachable u cluster
                closestUc = self.findClosestReachableUc(d, reachableUcs)
                closestUc.addElement(d)
                
            if self.timeToSendMessage(processedElements):
                # TODO send alist and olist to stage 2 !!!!!!!!!!!!!!!!!!!!
                self.sendListsToStage2()
                
                
      
    # returns a list of reachable u clusters for a given element          
    def findReachableUcs(self, d):
        
        reachableUcs = []
        
        self.checkReachabilityFrom(self.aList, d, reachableUcs)
                       
        if not reachableUcs:
            # empty list -> check oList
            self.checkReachabilityFrom(self.oList, d, reachableUcs)
            
            
            
    # modifies reareachableUcs iterating over a given list of u clusters
    def checkReachabilityFrom(self, uCsList, d, reachableUcs):
         for uC in uCsList:
            # the uC has the parametrized relative size
            if uC.isReachableFrom(d):
                reachableUcs.append(uC)
                
                
 
    # returns the closest uC for an element, given a set of reachable uCs
    def findClosestReachableUc(self, d, reachableUcs):
        closestUc = None
        minDistance = float("inf")
        
        for uC in reachableUcs:
            distance = self.manhatanDistance(d, uC)
            if distance < minDistance:
                minDistance = distance
                closestUc = uC
        
        return closestUc
        
        
    
    # returns the manhatan distance between a cluster and an element
    def manhatanDistance(self, d, uC):
        dist = 0
        # for every feature/dimension
        for i in range(len(d)):
            diff = d[i] - uC.getICentroid(i)
            dist = dist + abs(diff)
            
        return dist
        
    
    
    # returns true if it's time to send message to stage 2
    def timeToSendMessage(self, processedElements):
       return processedElements == self.tGlobal