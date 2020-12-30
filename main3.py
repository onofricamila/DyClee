# TAXIS DATA SET CLUSTERING -------------------------------------------------------------------------

from utils.dyclee import Dyclee
from utils.persistor import resetStorage
from config import getClusteringResultsPath, getDycleeName, getRealDatasetName, getTimeSeriesDatasetsPath
import numpy as np
from utils.bounding_box import BoundingBox
from utils.plotter import Plotter
from utils.prepare_result import prepareResultFrom
import matplotlib.pyplot as plt
import pandas as pd
from utils.helpers.custom_printing_fxs import printInGreen
import datetime

# fx
def validate_centroid(centroid, min_lat = 13, max_lat = 15, min_long = 59, max_long = 64):  # bounding box de la zona que no quiero
    return  not (min_lat <= centroid[0] <= max_lat) & (min_long <= centroid[1] <= max_long)


def filter_unwanted_ones(microclusters):
    return [mc for mc in microclusters if validate_centroid(mc.getCentroid())]


def validate_timestamp(timestamp, date = datetime.datetime(2018, 10, 2, 9)):
     return timestamp > date

def validate_longitude(longitude, min = 55.3617373725, max = 69.1062472602):
    return min <= longitude <= max


def validate_latitude(latitude, min = 11.0273686052, max = 23.9033785336):
    return min <= latitude <= max


def validate_boundaries(p):
    return validate_longitude(p.longitude) & validate_latitude(p.latitude)


# initialization
relativeSize=0.03         
speed = 5000
lambd = 0.4 # if it has a value over 0, when a micro cluster is updated, tl will be checked and the diff with current time will matter
periodicUpdateAt = 4 # float("inf")
timeWindow = 2 # float("inf")
periodicRemovalAt = 4 # 15
closenessThreshold = 1 # cuanto mas greande, menos pintas

# fetch real data set
# dataset = np.genfromtxt(getTimeSeriesDatasetsPath() + getRealDatasetName() + ".csv", delimiter=",", )
dataset = pd.read_csv(getTimeSeriesDatasetsPath() + getRealDatasetName() + ".csv", sep=',')
dataset['to_timestamp'] = dataset['to_timestamp'].astype('datetime64[ns]')
dataset = dataset[dataset['to_timestamp'].apply(validate_timestamp)]
# xmax, ymax = dataset.max(axis=0)
# xmin, ymin = dataset.min(axis=0)

# data context
dataContext = [ # FIXME: hardcodeamos los límites de sweden?
                BoundingBox(minimun=11.0273686052 , maximun=23.9033785336),
                BoundingBox(minimun=55.3617373725, maximun=69.1062472602),
            ]

dyclee = Dyclee(dataContext = dataContext, relativeSize = relativeSize, speed = speed, lambd = lambd,
                periodicRemovalAt = periodicRemovalAt, periodicUpdateAt = periodicUpdateAt,
                timeWindow = timeWindow, closenessThreshold = closenessThreshold)

tGlobal = 12000
ac = 0 # represents amount of processed elements
i = 0 # for tglobal
folder = getClusteringResultsPath() + getRealDatasetName() + '/' + getDycleeName() + '/'
# resetStorage(folder) # FIXME: uncomment

for ind, p in dataset.iterrows():
    if not validate_timestamp(p['to_timestamp']):       # para un análisis más rápido
        print(p, ' ... (no pasa por timestamp)')
        continue

    if not validate_boundaries(p):            # para descartar coordenadas fuera de sweden
        print(p, ' ... (no pasa por coordenadas)')
        continue

    ac += 1
    point = [p.latitude, p.longitude] # ahora esta completo el dataset, hay que subsetear
    dyclee.trainOnElement(point)

    if ac % tGlobal == 0:
        currMicroClusters = dyclee.getClusteringResult()
        currMicroClusters = filter_unwanted_ones(currMicroClusters) # para sacarme de encima los que arruinan el plot
        title = "CURRENT TIMESTAMP: " + p["to_timestamp"].isoformat() + "\n"
        res = prepareResultFrom(currMicroClusters)
        # storeTimeSeriesResult({"processedElements": ac, "result": res}, folder) # FIXME: uncomment!
        # FIXME: plotting outside dyclee
        p = Plotter(currMicroClusters, dataContext)
        ax = plt.gca() # we try the one with the mc size
        p.plotMicroClustersSize(ax)
        fig = plt.gcf()
        fig.canvas.manager.window.showMaximized()
        fig.suptitle(title, fontweight="bold")
        plt.show()

algoConfig = dyclee.getConfig()
# storeAlgoConfig(algoConfig, folder) # FIXME: uncomment!
