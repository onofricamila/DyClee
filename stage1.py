#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:35:06 2019

@author: camila
"""

from uCluster import uCluster
from customizedPrinting import printInBlueForDebugging

  
class Stage1:
    
    def __init__(self, s1ToS2ComQueue, s2ToS1ComQueue, dataContext, relativeSize=1, tGlobal=1):
        # communication instance variables    
        self.s1ToS2ComQueue = s1ToS2ComQueue
        self.s2ToS1ComQueue = s2ToS1ComQueue  
      
        # stage1 algo instance variables
        self.dataContext = dataContext
        self.relativeSize = relativeSize
        self.tGlobal = tGlobal        
        self.aList = []
        self.oList = []
        self.processedElements = 0
    
    
    # main method
    def formUcs(self, dataset):
    # ASSUMPTIONS: dataset es un vector de vectores    
        printInBlueForDebugging("S1 formUcs")
        
        for d in dataset:
            printInBlueForDebugging("S1 dataset element: " + d.__repr__())
            # processed_elements ++
            self.processedElements += 1
            
            self.checkUpdatedListsFromStage2()
            
            # find reachable u clusters for the new element
            reachableUcs = self.findReachableUcs(d)
            printInBlueForDebugging("S1 reachables: " + reachableUcs.__repr__())
            if not reachableUcs:
                # empty list -> create u cluster from element 
                # the uC will have the parametrized relative size
                uC = uCluster(self.relativeSize, d, self.dataContext)
                self.oList.append(uC)
                printInBlueForDebugging("S1 se creo u cluster: " + uC.__repr__())
                
            else: 
                # find closest reachable u cluster
                closestUc = self.findClosestReachableUc(d, reachableUcs)
                closestUc.addElement(d)
                printInBlueForDebugging("S1 closestUc: " + closestUc.__repr__())
            if self.timeToSendMessage():
                printInBlueForDebugging("S1 lists sent to s2")
                self.sendListsToStage2()
                self.resetProcessedElements()
        self.sendEndMsgToStage2()



    # checks if there's a msg from s2 so both u cluster lists must be updated
    def checkUpdatedListsFromStage2(self):
        printInBlueForDebugging("S1 checkUpdatedListsFromStage2")
        # to avoid unnecessary waiting
        if not self.s2ToS1ComQueue.empty():
            printInBlueForDebugging("S1 receiving lists from s2")
            lists = self.s2ToS1ComQueue.get()
            aList, oList = lists
            # update both lists              
            self.aList = aList    
            self.oList = oList  
            printInBlueForDebugging("alist: " + aList.__repr__())
            printInBlueForDebugging("olist: " + oList.__repr__())
            
            
      
    # returns a list of reachable u clusters for a given element          
    def findReachableUcs(self, d):
        
        reachableUcs = self.getReachableUcsFrom(self.aList, d)
                       
        if not reachableUcs:
            # empty list -> check oList
            reachableUcs = self.getReachableUcsFrom(self.oList, d)
        return reachableUcs
      
            
            
    # modifies reareachableUcs iterating over a given list of u clusters
    def getReachableUcsFrom(self, uCsList, d):
      res = []   
      for uC in uCsList:
            # the uC has the parametrized relative size
            if uC.isReachableFrom(d):
                res.append(uC)
      return res        
                
 
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
        uCCentroid = uC.getCentroid()
        # for every feature/dimension
        for i in range(len(d)):
            diff = d[i] - uCCentroid[i]
            dist = dist + abs(diff)
            
        return dist
        
    
    
    # returns true if it's time to send message to stage 2
    def timeToSendMessage(self):
       return self.processedElements == self.tGlobal
     
      
      
    def sendListsToStage2(self):
      self.s1ToS2ComQueue.put((self.aList, self.oList))
      
      
      
    def resetProcessedElements(self):
      self.processedElements = 0
      
      
      
    def sendEndMsgToStage2(self):
      self.s1ToS2ComQueue.put("DONE")
      
      
    