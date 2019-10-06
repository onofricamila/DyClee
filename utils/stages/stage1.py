#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:35:06 2019

@author: camila
"""

from utils.uClusters.uCluster import uCluster
from utils.helpers.customPrintingFxs import printInBlueForDebugging
from utils.helpers.customMathFxs import stddev
  
class Stage1:
    
    def __init__(self, s1ToS2ComQueue, s2ToS1ComQueue, relativeSize=1, tGlobal=1):
        # communication instance variables    
        self.s1ToS2ComQueue = s1ToS2ComQueue
        self.s2ToS1ComQueue = s2ToS1ComQueue  
      
        # stage1 algo instance variables
        self.relativeSize = relativeSize
        self.tGlobal = tGlobal        
        self.aList = []
        self.oList = []
        self.processedElements = 0
        
        # to be calculated when the dataset is received
        self.meanList = []
        self.SDList = []

    
    
    # main method
    def start(self, dataset):
        self.calculateMeanAndSD(dataset)
        scaledDataset = self.scaleDataset(dataset)
        self.formUcs(scaledDataset)
        
        
        
        
    def scaleDataset(self, dataset):
        res = []
        # for each element
        for i in range(len(dataset)):
            scaledEl = self.scaleDatasetElement(dataset[i])
            res.append(scaledEl) 
        return res
    

          
              
    def scaleDatasetElement(self, el):
        scaledEl = []
        # for each dimension
        for fIndex in range(len(el)):
            fValue = el[fIndex]
            scaledFeature = self.scaleDatasetElementFeature(fValue, fIndex)
            scaledEl.append(scaledFeature)
        return scaledEl
    
    
    
    
    def scaleDatasetElementFeature(self, fValue, fIndex):
        return (fValue - self.meanList[fIndex]) / self.SDList[fIndex]
        
    
    
    
    def formUcs(self, dataset):
    # ASSUMPTIONS: dataset es un vector de vectores    
        for d in dataset:
            # processed_elements ++
            self.processedElements += 1
            
            # find reachable u clusters for the new element
            reachableUcs = self.findReachableUcs(d)
            if not reachableUcs:
                # empty list -> create u cluster from element 
                # the uC will have the parametrized relative size
                uC = uCluster(self.relativeSize, d)
                self.oList.append(uC)
                
            else: 
                # find closest reachable u cluster
                closestUc = self.findClosestReachableUc(d, reachableUcs)
                closestUc.addElement(d)
            if self.timeToSendMessage():
                printInBlueForDebugging("S1 lists sent to s2")
                self.sendListsToStage2()
                self.resetProcessedElements()
                self.checkUpdatedListsFromStage2()
        # TODO: remove the following block when workiing w streams
        if len(dataset) < self.tGlobal:
          self.sendListsToStage2()
        self.sendEndMsgToStage2()




    def calculateMeanAndSD(self, dataset):
        n = len(dataset)
        # sample taken to get the ammount of features
        anElement = dataset[0]
        # for each feature
        for fIndex in range(len(anElement)):
            acPerFeature = 0
            fValuesList = []
            # for each element in dataset
            for i in range(n):  
                el = dataset[i]
                fValue = el[fIndex]
                acPerFeature += fValue
                # to later obtain ssdev
                fValuesList.append(fValue)
                
            featureMean = acPerFeature / n
            self.meanList.append(featureMean)
            featureSD = stddev(data=fValuesList, mean=featureMean)
            self.SDList.append(featureSD)

        


    # checks if there's a msg from s2 so both u cluster lists must be updated
    def checkUpdatedListsFromStage2(self):
          printInBlueForDebugging("S1 waiting for lists from s2")
          lists = self.s2ToS1ComQueue.get()
          aList, oList = lists
          # update both lists              
          self.aList = aList    
          self.oList = oList  
            
            
      
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
      
      
    