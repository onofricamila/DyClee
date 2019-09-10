#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:35:06 2019

@author: camila
"""
import numpy as np


class Stage1:
    
    
    # The __init__() function is called automatically every time the class is being used to create a new object.
    def __init__(self, relativeSize, tGlobal):
        self.relativeSize = relativeSize
        self.tGlobal = tGlobal        
        
    
    
    def formUcs(self, dataset):
        
        aList = []
        oList = []
        processedElements = 0
        
        for d in dataset:
            # processed_elements ++
            processedElements += 1
            
            # TODO receive updated lists from stage 2 !!!!!!!!!!!!!!!!!!!!
            
            # find reachable u clusters for the new element
            reachableUcs = self.findReachableUcs(dataset, d, self.relativeSize, aList, oList)
            
            if not reachableUcs:
                # empty list -> create u cluster from element
                uC = self.createUc(self, d)
                oList.append(uC) 
                
            else: 
                # find closest reachable u cluster
                closestUc = self.findClosestReachableUc(d, reachableUcs)
                self.updateUc(closestUc, d)
                
            if self.timeToSendMessage(processedElements, self.tGlobal):
                
                # TODO send alist and olist to stage 2 !!!!!!!!!!!!!!!!!!!!


    