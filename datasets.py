#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 20:03:56 2019

@author: camila
"""
from sklearn import datasets

# Datasets for testing --------------------------------------------------------

# pilot 
pilot = [[2, 10]]

# test forming 2 uCs
forming2uCs = [[2, 10], [80, 100]]

# test adding element to uC (notice change in D)
addingElToUc = [[2, 10], [1, 9]]

# test choosing closest reachable uC
choosingClosestReachableUc = [[2, 10], [11, 19], [7, 15]]

# test going from uC to noise
fromUcToNoise = [[2, 10], [80, 100], [1, 9]]

# test going from uC to noise with more data
fromUcToNoiseV2 = [[2, 10], [1, 9], [80, 100], [83, 98], [5, 13]]

# test forming many uCs
formingManyUcs = [[2, 10], [30, 40], [1, 9], [80, 100]]


# min and max for each feature
testingDatasetsContext = [[0, 100], [0, 100]]



# Sklearn datasets ------------------------------------------------------------

nSamples = 1500
noise = None # 0.05



# noisy circles
noisy_circles = datasets.make_circles(n_samples=nSamples, factor=0.3, noise=noise)[0]
noisyCirclesDataset = noisy_circles.tolist()

x,y = zip(*noisyCirclesDataset)

maxX = max(x)
maxY = max(y)
minX = min(x)
minY = min(y)

noisyCirclesDatasetContext = [[minX, maxX], [minY, maxY]]



# noisy moons
noisy_moons = datasets.make_moons(n_samples=nSamples, noise=noise)[0]
noisyMoonsDataset = noisy_moons.tolist()

x,y = zip(*noisyMoonsDataset)

maxX = max(x)
maxY = max(y)
minX = min(x)
minY = min(y)

noisyMoonsDatasetContext = [[minX, maxX], [minY, maxY]]



# blobs
noisy_circles = datasets.make_blobs(n_samples=nSamples)[0]
blobsDataset = noisy_circles.tolist()

x,y = zip(*blobsDataset)

maxX = max(x)
maxY = max(y)
minX = min(x)
minY = min(y)

blobsDatasetContext = [[minX, maxX], [minY, maxY]]




















