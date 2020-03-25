from datasets.sklearnDatasets import noisyCirclesDataset, noisyMoonsDataset, blobsDataset
from datasets.customCircunferencesDataset import customCircunferencesDataset
from utils.dataset_fetcher import getTimeSeriesDatasetFromFolder
from utils.dyclee import Dyclee
from sklearn.preprocessing import StandardScaler
from utils.persistor import resetStorage, storeAlgoConfig, storeResult
import numpy as np

# ALGORITHM INITIALIZATION
relativeSize=0.03
speed = 50
uncommonDimensions = 0
lambd = 0.7 # if it has a value over 0, when a micro cluster is updated, tl will be checked and the diff with current time will matter
periodicRemovalAt = 200 # 201 # 500000 # exaggerated to not to remove outliers
periodicUpdateAt = 100 # 99 # 2500000 # exaggerated to not to apply forgetting component to micro clusters that have not been updated in a while
microClustersDtThreshold = 5
findNotDirectlyConnButCloseMicroClusters = True
distToAllStdevProportion4Painting = 0.8


dyclee = Dyclee(relativeSize=relativeSize, speed = speed, uncommonDimensions = uncommonDimensions, lambd = lambd,
                periodicRemovalAt = periodicRemovalAt, periodicUpdateAt = periodicUpdateAt,
                microClustersDtThreshold = microClustersDtThreshold, findNotDirectlyConnButCloseMicroClusters = findNotDirectlyConnButCloseMicroClusters,
                distToAllStdevProportion4Painting = distToAllStdevProportion4Painting)

# store algo config
algoConfig = {
    "relativeSize": relativeSize,
    "speed": speed,
    "uncommonDimensions": uncommonDimensions,
    "lambd": lambd,
    "periodicRemovalAt": periodicRemovalAt,
    "periodicUpdateAt": periodicUpdateAt,
}
storeAlgoConfig(algoConfig)


# NON TIME SERIES DATA SETS CLUSTERING ---------------------------------------------------------------------

# ac = 0 # processed samples
#
# scaler = StandardScaler()
# dataset = noisyMoonsDataset
# tGlobal = len(dataset)
#
# for d in scaler.fit_transform(dataset):
#     ac += 1
#     dyclee.trainOnElement(d)
#     if ac % tGlobal == 0:
#         dyclee.getClusteringResult()
        

# TIME SERIES DATA SET CLUSTERING -------------------------------------------------------------------------

def prepareResultFrom(currMicroClusters):
    res = []
    for mc in currMicroClusters:
        centroid = mc.getCentroid()
        label = mc.label
        row = [centroid[0], centroid[1], label]
        res.append(row)
    return np.array(res)

tGlobal = 200
ac = 0 # represents amount of processed elements

for point in getTimeSeriesDatasetFromFolder():
    ac += 1
    dyclee.trainOnElement(point)
    if ac % tGlobal == 0:
        currMicroClusters = dyclee.getClusteringResult()
        res = prepareResultFrom(currMicroClusters)
        storeResult({"processedElements": ac, "result": res})
