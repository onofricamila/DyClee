from datasets.sklearnDatasets import noisyCirclesDataset, noisyMoonsDataset, blobsDataset
from datasets.customCircunferencesDataset import customCircunferencesDataset
from utils.dataset_fetcher import getTimeSeriesDatasetFromFolder
from utils.dyclee import Dyclee
from sklearn.preprocessing import StandardScaler
from utils.persistor import resetStorage, storeAlgoConfig, storeResult
import numpy as np

relativeSize=0.03
speed = 25
uncommonDimensions = 0
lambd = 0.7 # bc if it has a value over 0, when a micro cluster is updated tl will be checked and the diff with current time will matter
periodicRemovalAt = 201 # 500000 # exaggerated to not to remove outliers
periodicUpdateAt = 99 # 2500000 # exaggerated to not to apply forgetting component to micro clusters that have not been updated in a while
microClustersDtThreshold = 5
findNotDirectlyConnButCloseMicroClusters = True
distToAllStdevProportion4Painting = 1


dc = Dyclee(relativeSize=relativeSize, speed = speed, uncommonDimensions = uncommonDimensions, lambd = lambd,
            periodicRemovalAt = periodicRemovalAt, periodicUpdateAt = periodicUpdateAt,
            microClustersDtThreshold = microClustersDtThreshold, findNotDirectlyConnButCloseMicroClusters = findNotDirectlyConnButCloseMicroClusters,
            distToAllStdevProportion4Painting = distToAllStdevProportion4Painting)

# ac = 0 # processed samples

# for the sklearn datasets
# scaler = StandardScaler()
# dataset = noisyMoonsDataset
# tGlobal = len(dataset)

# for d in scaler.fit_transform(dataset):
#     ac += 1
#     dc.trainOnElement(d)
#     if ac % tGlobal == 0:
#         dc.getClusteringResult()

# tGlobal = 200
# for d in customCircunferencesDataset:
#     ac += 1
#     dc.trainOnElement(d)
#     if ac % tGlobal == 0:
#         dc.getClusteringResult()


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

# get the data
X = getTimeSeriesDatasetFromFolder()

batch = []
tGlobal = 200
ac = 0
time = 0


def prepareResultFrom(currMicroClusters):
    res = []
    for mc in currMicroClusters:
        centroid = mc.getCentroid()
        label = mc.label
        row = [centroid[0], centroid[1], label]
        res.append(row)
    return np.array(res)


for d in getTimeSeriesDatasetFromFolder():
    # increment amount of processed elements
    ac += 1
    dc.trainOnElement(d)
    if ac % tGlobal == 0:
        currMicroClusters = dc.getClusteringResult()
        time = time + tGlobal
        res = prepareResultFrom(currMicroClusters)
        storeResult({"time": time, "result": res})
