from datasets.simpleDatasets import dsChoosingClosestReachableUc, dsForming2uCs, dsFromUcToNoise, dsPilot
from datasets.sklearnDatasets import noisyCirclesDataset, noisyMoonsDataset, blobsDataset

chosenDataset = noisyMoonsDataset

rs = 0.06

tG = 1500

uncdim = 0