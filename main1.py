# NON TIME SERIES DATA SETS CLUSTERING ---------------------------------------------------------------------

from sklearn.preprocessing import StandardScaler
from utils.non_time_series_datasets_fetcher import getDatasetsFromFolder
from utils.dyclee import Dyclee
from params_config import getClusteringResultsPath, getDycleeName, getNonTimeSeriesDatasetsPath
from utils.bounding_box import BoundingBox
from utils.prepare_result import prepareResultFrom
from utils.plotter import Plotter
import matplotlib.pyplot as plt

# params
relativeSize=0.06
uncommonDimensions = 0
closenessThreshold = 1.5

# obtain the data sets from the csv files
non_time_series_datasets = getDatasetsFromFolder(getNonTimeSeriesDatasetsPath())
# data context
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
  #  storeNonTimeSeriesResult(res, folder) # FIXME: uncomment!
    # store algo config
    algoConfig = dyclee.getConfig()
  #  storeAlgoConfig(algoConfig, folder) # FIXME: uncomment!
    # IMPORTANT: plotting outside dyclee
    p = Plotter(currMicroClusters, dataContext)
    # p.plotClusters() # FIXME: uncomment if you want all 3 plots to be displayed - and comment the whole following block
    ax = plt.gca() # we try the one with the mc size
    p.plotMicroClustersSize(ax)
    plt.show()

