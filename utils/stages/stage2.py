#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from utils.helpers.customPrintingFxs import printInMagenta

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




  def resetLabelsAsUnclass(self, uCs):
    for uC in uCs:
      uC.label = -1




  def calculateMeanFor(self, uCs):
    return np.mean([uC.CF.D for uC in uCs])

  def calculateMedianFor(self, uCs):
    return np.median([uC.CF.D for uC in uCs])




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
    return [uC for uC in uCs if self.isDense(uC)]




  def findDirectlyConnectedUcsFor(self, uC, uCs):
    res = []
    for u in uCs:
      if uC.isDirectlyConnectedWith(u, self.uncommonDimensions):
        res.append(u)
    return res




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
      if denseUc not in alreadySeen:
        alreadySeen.append(denseUc)
        currentClusterId += 1
        denseUc.label = currentClusterId
        connectedUcs = self.findDirectlyConnectedUcsFor(denseUc, updatedAList)
        self.growCluster(currentClusterId, alreadySeen, connectedUcs, updatedAList)
    # for loop finished -> clusters were formed
    self.plotClusters(uCs)




  def growCluster(self, currentClusterId, alreadySeen, connectedUcs, uCs):
    i = 0
    while i < len(connectedUcs):
      conUc = connectedUcs[i]
      if (conUc not in alreadySeen):
        conUc.label = currentClusterId
        alreadySeen.append(conUc)
        if self.isDense(conUc):
          newConnectedUcs = self.findDirectlyConnectedUcsFor(conUc, uCs)
          for newNeighbour in newConnectedUcs:
            connectedUcs.append(newNeighbour)
      i += 1
    


          
  # plots current clusters          
  def plotClusters(self, uCs):
    self.scatter(uCs)
    # set axes limits
    minAndMaxDeviations = [-2.5, 2.5]
    axes = plt.gca()
    axes.set_xlim(minAndMaxDeviations)
    axes.set_ylim(minAndMaxDeviations)
    # set plot general characteristics
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.grid(color='k', linestyle=':', linewidth=1)
    plt.show()




  def getMarkersSizeList(self, uCs):
    res = []
    for uC in uCs:
      if self.isOutlier(uC):
        # really small size -> comes out almost as a point
        res.append(5)
      elif self.isSemiDense(uC):
        # big marker
        res.append(20)
      elif self.isDense(uC):
        # medium size marker
        res.append(50)
    return res




  def scatter(self, uCs):
    if not self.plottableUcs(uCs):
      return
    # let's plot!
    # first set markers size to represent different densities
    s = self.getMarkersSizeList(uCs)
    # then get a list with u cluster labels
    labelsPerUCluster = [uC.label for uC in uCs]
    # clusters will be a sequence of numbers (cluster number or -1) for each point in the dataset
    clusters = np.array(labelsPerUCluster)
    self.showPlotInfo(labelsPerUCluster)
    printInMagenta("* uCs labels: " + '\n' + clusters.__repr__() + '\n')
    # get uCs centroids
    centroids = [uC.getCentroid() for uC in uCs]
    x, y = zip(*centroids)
    printInMagenta("* uCs 'x' coordinates: " + '\n' + x.__repr__() + '\n')
    printInMagenta("* uCs 'y' coordinates: " + '\n' + y.__repr__())
    # scatter'
    plt.scatter(x, y, c=clusters, cmap="nipy_spectral", marker='s', alpha=0.8, s=s)




  def showPlotInfo(self, labelsPerUCluster):
    # final clusters info
    dic = self.clustersElCounter(labelsPerUCluster)
    dicLength = len(dic)
    if dicLength == 1:
      msg = "There is only 1 final cluster and "
    else:
      msg = "There are " + len(dic).__repr__() + " final clusters and "
    if -1 in labelsPerUCluster:
      msg += "one of them represents outliers (the black one)."
    else:
      msg += "no outliers."
    printInMagenta(msg + "\n")
    for key, value in dic.items():
      printInMagenta("- Cluster n°" + key.__repr__() + " -> " + value.__repr__() + " uCs" + "\n")




  def clustersElCounter(self, labelsPerUCluster):
    dicKeys = set(labelsPerUCluster)
    dic = {key: 0 for key in dicKeys}
    for c in labelsPerUCluster:
      dic[c] += 1
    return dic




  def plottableUcs(self, uCs):
    if len(uCs) == 0:
      # there are't any u clusters to plot
      return False
    firstEl = uCs[0]
    if len(firstEl.CF.LS) != 2:
      print("UNABLE TO DRAW CLUSTERS: IT'S NOT A 2D DATASET")
      return False
    # uCs are plottable
    return True