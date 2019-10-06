#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sklearn import datasets

# Global config
nSamples = 1500
noise = 0.06



# Noisy circles
noisy_circles = datasets.make_circles(n_samples=nSamples, factor=0.3, noise=noise)[0]
noisyCirclesDataset = noisy_circles.tolist()
# data context
x,y = zip(*noisyCirclesDataset)
maxX = max(x)
maxY = max(y)
minX = min(x)
minY = min(y)
noisyCirclesDatasetContext = [[minX, maxX], [minY, maxY]]



# Noisy moons
noisy_moons = datasets.make_moons(n_samples=nSamples, noise=noise)[0]
noisyMoonsDataset = noisy_moons.tolist()
# data context
x,y = zip(*noisyMoonsDataset)
maxX = max(x)
maxY = max(y)
minX = min(x)
minY = min(y)
noisyMoonsDatasetContext = [[minX, maxX], [minY, maxY]]



# Blobs
noisy_circles = datasets.make_blobs(n_samples=nSamples)[0]
blobsDataset = noisy_circles.tolist()
# data context
x,y = zip(*blobsDataset)
maxX = max(x)
maxY = max(y)
minX = min(x)
minY = min(y)
blobsDatasetContext = [[minX, maxX], [minY, maxY]]