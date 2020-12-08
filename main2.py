# TIME SERIES DATA SET CLUSTERING -------------------------------------------------------------------------
from utils.plotter import Plotter
from utils.time_series_dataset_fetcher import getTimeSeriesDatasetFromFolder
from utils.dyclee import Dyclee
from config import getClusteringResultsPath, getDycleeName, getTimeSeriesToyDatasetName
from utils.bounding_box import BoundingBox
from utils.prepare_result import prepareResultFrom


# initialization
relativeSize=0.02
speed = 50
lambd = 0.7 # if it has a value over 0, when a micro cluster is updated, tl will be checked and the diff with current time will matter
periodicUpdateAt = 2
timeWindow = 4
periodicRemovalAt = 4
closenessThreshold = 0.8

# data context
dataContext = [BoundingBox(minimun=-2 , maximun=2),
               BoundingBox(minimun=-2 , maximun=2)]

dyclee = Dyclee(dataContext = dataContext, relativeSize = relativeSize, speed = speed, lambd = lambd,
                periodicRemovalAt = periodicRemovalAt, periodicUpdateAt = periodicUpdateAt,
                timeWindow = timeWindow, closenessThreshold = closenessThreshold)

tGlobal = 200
ac = 0 # represents amount of processed elements
folder = getClusteringResultsPath() + getTimeSeriesToyDatasetName() + '/' + getDycleeName() + '/'

for point in getTimeSeriesDatasetFromFolder():
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

