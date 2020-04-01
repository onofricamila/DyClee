from datasets.sklearnDatasets import noisyCirclesDataset, noisyMoonsDataset, blobsDataset
from datasets.customCircunferencesDataset import customCircunferencesDataset
from utils.dataset_fetcher import getTimeSeriesDatasetFromFolder
from utils.dyclee import Dyclee
from sklearn.preprocessing import StandardScaler
from utils.persistor import resetStorage, storeAlgoConfig, storeNonTimeSeriesResult, storeTimeSeriesResult
from utils.datasets_fetcher import getDatasetsFromFolder
from config import getNonTimeSeriesDatasetsPath, getClusteringResultsPath, getDycleeName, getTimeSeriesToyDatasetName
import numpy as np

def prepareResultFrom(currMicroClusters):
    res = []
    for mc in currMicroClusters:
        centroid = mc.getCentroid()
        label = mc.label
        row = [centroid[0], centroid[1], label]
        res.append(row)
    return np.array(res)


# NON TIME SERIES DATA SETS CLUSTERING ---------------------------------------------------------------------
# params
# relativeSize=0.06
# speed = float("inf")
# uncommonDimensions = 0
# lambd = 0 # if it has a value over 0, when a micro cluster is updated, tl will be checked and the diff with current time will matter
# periodicUpdateAt = float("inf") # exaggerated to not to apply forgetting component to micro clusters that have not been updated in a while
# microClustersDtThreshold = 5
# periodicRemovalAt = float("inf") # exaggerated to not to remove outliers
# findNotDirectlyConnButCloseMicroClusters = True
# distToAllStdevProportion4Painting = 1.5
#
# # algo config
# algoConfig = {
#     "relativeSize": relativeSize,
#     "uncommonDimensions": uncommonDimensions,
# }
#
# # obtain the data sets from the csv files
# non_time_series_datasets = getDatasetsFromFolder(getNonTimeSeriesDatasetsPath())
#
# # iterate over the data sets
# for datIndx in range(len(non_time_series_datasets)):
#     # new dyclee for each data set
#     dyclee = Dyclee(relativeSize=relativeSize, speed=speed, uncommonDimensions=uncommonDimensions, lambd=lambd,
#                     periodicRemovalAt=periodicRemovalAt, periodicUpdateAt=periodicUpdateAt,
#                     microClustersDtThreshold=microClustersDtThreshold,
#                     findNotDirectlyConnButCloseMicroClusters=findNotDirectlyConnButCloseMicroClusters,
#                     distToAllStdevProportion4Painting=distToAllStdevProportion4Painting)
#     # start
#     X = non_time_series_datasets[datIndx]['dataset']
#     dName = non_time_series_datasets[datIndx]['name']
#     k = non_time_series_datasets[datIndx]['k']
#     baseFolder = getClusteringResultsPath() + dName + '/'
#     # normalize dataset for easier parameter selection
#     X = StandardScaler().fit_transform(X)
#     ac = 0 # processed samples
#     # iterate over the data points
#     for dataPoint in X:  # column index
#         ac += 1
#         dyclee.trainOnElement(dataPoint)
#     currMicroClusters = dyclee.getClusteringResult() # we wanna show the clustering at the end, only once
#     res = prepareResultFrom(currMicroClusters)
#     folder = baseFolder + getDycleeName() + '/'
#     storeNonTimeSeriesResult(res, folder)
#     # store algo config
#     storeAlgoConfig(algoConfig, folder)
#


# TIME SERIES DATA SET CLUSTERING -------------------------------------------------------------------------
# initialization
relativeSize=0.02
speed = 50
uncommonDimensions = 0
lambd = 0.7 # if it has a value over 0, when a micro cluster is updated, tl will be checked and the diff with current time will matter
periodicUpdateAt = 100 # 99 # 500000 # exaggerated to not to apply forgetting component to micro clusters that have not been updated in a while
microClustersDtThreshold = 4
periodicRemovalAt = 200 # 201 # 500000 # exaggerated to not to remove outliers
findNotDirectlyConnButCloseMicroClusters = True
distToAllStdevProportion4Painting = 0.8


dyclee = Dyclee(relativeSize=relativeSize, speed = speed, uncommonDimensions = uncommonDimensions, lambd = lambd,
                periodicRemovalAt = periodicRemovalAt, periodicUpdateAt = periodicUpdateAt,
                microClustersDtThreshold = microClustersDtThreshold, findNotDirectlyConnButCloseMicroClusters = findNotDirectlyConnButCloseMicroClusters,
                distToAllStdevProportion4Painting = distToAllStdevProportion4Painting)

# algo config
algoConfig = {
    "relativeSize": relativeSize,
    "speed": speed,
    "lambd": lambd,
    "periodicUpdateAt": periodicUpdateAt,
    "microClustersDtThreshold": microClustersDtThreshold,
    "periodicRemovalAt": periodicRemovalAt,
    "distToAllStdevProportion4Painting": distToAllStdevProportion4Painting,
}

tGlobal = 200
ac = 0 # represents amount of processed elements
folder = getClusteringResultsPath() + getTimeSeriesToyDatasetName() + '/' + getDycleeName() + '/'

for point in getTimeSeriesDatasetFromFolder():
    ac += 1
    dyclee.trainOnElement(point)
    if ac % tGlobal == 0:
        currMicroClusters = dyclee.getClusteringResult()
        res = prepareResultFrom(currMicroClusters)
        storeTimeSeriesResult({"processedElements": ac, "result": res}, folder)
storeAlgoConfig(algoConfig, folder)
