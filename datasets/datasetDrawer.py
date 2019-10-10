import matplotlib.pyplot as plt
from datasets.customCircunferencesDataset import customCircunferencesDataset
from datasets.simpleDatasets import dsPilot, dsChoosingClosestReachableUc, dsForming2uCs, dsFromUcToNoise
from datasets.sklearnDatasets import noisyCirclesDataset, noisyMoonsDataset, blobsDataset

datasetToDraw = customCircunferencesDataset

x, y = zip(*datasetToDraw)
plt.plot(x, y, "o", alpha=0.5,)
plt.show()