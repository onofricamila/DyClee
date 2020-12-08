# TAXIS DATA SET CLUSTERING -------------------------------------------------------------------------

from utils.dyclee import Dyclee
from utils.persistor import resetStorage
from config import getClusteringResultsPath, getDycleeName, getRealDatasetName, getTimeSeriesDatasetsPath
import numpy as np
from utils.bounding_box import BoundingBox
from utils.plotter import Plotter
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
        # storeTimeSeriesResult({"processedElements": ac, "result": res}, folder) # FIXME: uncomment!
        # FIXME: plotting outside dyclee
        p = Plotter(currMicroClusters, dataContext)
        p.plotClusters()
algoConfig = dyclee.getConfig()
# storeAlgoConfig(algoConfig, folder) # FIXME: uncomment!
