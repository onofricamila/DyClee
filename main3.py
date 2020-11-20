# TAXIS DATA SET CLUSTERING -------------------------------------------------------------------------

from sklearn.preprocessing import StandardScaler
from utils.non_time_series_datasets_fetcher import getDatasetsFromFolder
from utils.time_series_dataset_fetcher import getTimeSeriesDatasetFromFolder
from utils.dyclee import Dyclee
from utils.persistor import storeAlgoConfig, storeTimeSeriesResult, storeNonTimeSeriesResult, resetStorage
from config import getClusteringResultsPath, getDycleeName, getTimeSeriesToyDatasetName, getNonTimeSeriesDatasetsPath, \
    getRealDatasetName, getTimeSeriesDatasetsPath
import numpy as np
from utils.bounding_box import BoundingBox
from utils.prepare_result import prepareResultFrom

# initialization
relativeSize=0.00009
speed = 500
lambd = 0.75 # if it has a value over 0, when a micro cluster is updated, tl will be checked and the diff with current time will matter
periodicUpdateAt = 3 # float("inf")
timeWindow = 3 # float("inf")
periodicRemovalAt = 3 # float("inf")
closenessThreshold = 0.5

# fetch real data set
dataset = np.genfromtxt(getTimeSeriesDatasetsPath() + getRealDatasetName() + ".csv", delimiter=",", )

xmax, ymax = dataset.max(axis=0)
xmin, ymin = dataset.min(axis=0)

# data context
dataContext = [BoundingBox(minimun=xmin , maximun=xmax),
               BoundingBox(minimun=ymin , maximun=ymax)]

dyclee = Dyclee(dataContext = dataContext, relativeSize = relativeSize, speed = speed, lambd = lambd,
                periodicRemovalAt = periodicRemovalAt, periodicUpdateAt = periodicUpdateAt,
                timeWindow = timeWindow, closenessThreshold = closenessThreshold)

tGlobal = 75000
ac = 0 # represents amount of processed elements
folder = getClusteringResultsPath() + getRealDatasetName() + '/' + getDycleeName() + '/'
resetStorage(folder)
for point in dataset:
    ac += 1
    dyclee.trainOnElement(point)
    if ac % tGlobal == 0:
        currMicroClusters = dyclee.getClusteringResult()
        res = prepareResultFrom(currMicroClusters)
        storeTimeSeriesResult({"processedElements": ac, "result": res}, folder)
algoConfig = dyclee.getConfig()
storeAlgoConfig(algoConfig, folder)
