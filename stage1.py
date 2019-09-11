#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:35:06 2019

@author: camila
"""

# TODO finish uC class !!!!!!!!!!!!!!!!!!!!

import numpy as np
from uCluster import uCluster

class Stage1:
    
    
    # The __init__() function is called automatically every time the class is being used to create a new object.
    def __init__(self, relativeSize, tGlobal):
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
                self.updateUc(closestUc, d)
                
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
                
                
 
    