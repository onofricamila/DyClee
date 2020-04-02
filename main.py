from sklearn.preprocessing import StandardScaler
from utils.non_time_series_datasets_fetcher import getDatasetsFromFolder
from utils.time_series_dataset_fetcher import getTimeSeriesDatasetFromFolder
from utils.dyclee import Dyclee
from utils.persistor import storeAlgoConfig, storeTimeSeriesResult, storeNonTimeSeriesResult
from config import getClusteringResultsPath, getDycleeName, getTimeSeriesToyDatasetName, getNonTimeSeriesDatasetsPath
import numpy as np
from utils.bounding_box import BoundingBox

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
relativeSize=0.06
uncommonDimensions = 0
closenessThreshold = 1.5

# obtain the data sets from the csv files
non_time_series_datasets = getDatasetsFromFolder(getNonTimeSeriesDatasetsPath())
#data context
dataContext = [BoundingBox(minimun=-2 , maximun=2),
               BoundingBox(minimun=-2 , maximun=2)]

# iterate over the data sets
for datIndx in range(len(non_time_series_datasets)):
    # new dyclee for each data set
    dyclee = Dyclee(dataContext=dataContext, relativeSize=relativeSize, uncommonDimensions=uncommonDimensions,
                    closenessThreshold=closenessThreshold)
    # start
    X = non_time_series_datasets[datIndx]['dataset']
    dName = non_time_series_datasets[datIndx]['name']
    k = non_time_series_datasets[datIndx]['k']
    baseFolder = getClusteringResultsPath() + dName + '/'
    # normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(X)
    ac = 0 # processed samples
    # iterate over the data points
    for dataPoint in X:  # column index
        ac += 1
        dyclee.trainOnElement(dataPoint)
    currMicroClusters = dyclee.getClusteringResult() # we wanna show the clustering at the end, only once
    res = prepareResultFrom(currMicroClusters)
    folder = baseFolder + getDycleeName() + '/'
    storeNonTimeSeriesResult(res, folder)
    # store algo config
    algoConfig = dyclee.getConfig()
    storeAlgoConfig(algoConfig, folder)



# # TIME SERIES DATA SET CLUSTERING -------------------------------------------------------------------------
# # initialization
# relativeSize=0.02
# speed = 50
# lambd = 0.7 # if it has a value over 0, when a micro cluster is updated, tl will be checked and the diff with current time will matter
# periodicUpdateAt = 2
# timeWindow = 4
# periodicRemovalAt = 4
# closenessThreshold = 0.8
#
# #data context
# dataContext = [BoundingBox(minimun=-2 , maximun=2),
#                BoundingBox(minimun=-2 , maximun=2)]
#
# dyclee = Dyclee(dataContext = dataContext, relativeSize = relativeSize, speed = speed, lambd = lambd,
#                 periodicRemovalAt = periodicRemovalAt, periodicUpdateAt = periodicUpdateAt,
#                 timeWindow = timeWindow, closenessThreshold = closenessThreshold)
#
# tGlobal = 200
# ac = 0 # represents amount of processed elements
# folder = getClusteringResultsPath() + getTimeSeriesToyDatasetName() + '/' + getDycleeName() + '/'
#
# for point in getTimeSeriesDatasetFromFolder():
#     ac += 1
#     dyclee.trainOnElement(point)
#     if ac % tGlobal == 0:
#         currMicroClusters = dyclee.getClusteringResult()
#         res = prepareResultFrom(currMicroClusters)
#         storeTimeSeriesResult({"processedElements": ac, "result": res}, folder)
# algoConfig = dyclee.getConfig()
# storeAlgoConfig(algoConfig, folder)
