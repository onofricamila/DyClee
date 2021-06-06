# TAXIS DATA SET TIME SERIES CLUSTERING -------------------------------------------------------------------------
from time import sleep
from mpl_toolkits.basemap import Basemap
from params_config import big_mc, medium_mc, small_mc, micro_mc
from utils.dyclee import Dyclee
from utils.gif_maker import generate_gif
from utils.persistor import resetStorage, resetFolderContent, storeAlgoConfig
from config import getClusteringResultsPath, getDycleeName, getRealDatasetName, getTimeSeriesDatasetsPath
from utils.bounding_box import BoundingBox
from utils.plotter import Plotter
from utils.prepare_result import prepareResultFrom
import matplotlib.pyplot as plt
import pandas as pd
import datetime

# config
generate_gif = False
will_calculate_DBCV = False

# algo initialization
params = big_mc.params # chosen hyper parmas config
results_path = big_mc.results_path # chosen location to store figures and gif

# filter unwanted mc
def validate_centroid(centroid, min_lat = 13, max_lat = 15, min_long = 59, max_long = 64):  # bounding box de la zona que no quiero
    return  not (min_lat <= centroid[0] <= max_lat) & (min_long <= centroid[1] <= max_long) and not (21 <= centroid[0] <= 23) & (64 <= centroid[1] <= 66)

def filter_unwanted_ones(microclusters):
    return [mc for mc in microclusters if validate_centroid(mc.getCentroid())]


# timestamp
def validate_timestamp(timestamp, date):
     return timestamp > date

# end timestamp
def end(timestamp, date = datetime.datetime(2018, 10, 2, 20, 30)):
     return timestamp > date


# boundaries: sweden
def validate_longitude(longitude, min = 55.3617373725, max = 69.1062472602):
    return min <= longitude <= max

def validate_latitude(latitude, min = 11.0273686052, max = 23.9033785336):
    return min <= latitude <= max

def validate_boundaries(p):
    return validate_longitude(p.longitude) & validate_latitude(p.latitude)


# validate point: coordinates + day
def validate_p(p):
    return validate_timestamp(p['to_timestamp'], date = datetime.datetime(2018, 10, 2)) & validate_boundaries(p)


# plot micro clusters size with sweden's map as background
def plot_with_map(currMicroClusters, dataContext, title):
    p = Plotter(currMicroClusters, dataContext)
    ax = plt.gca()  # we try the one with the mc size
    # map
    map = Basemap(projection='cyl', )
    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='gray', lake_color='aqua')
    map.drawcoastlines()
    # plot
    p.plotMicroClustersSize(ax)
    fig = plt.gcf()
    fig.canvas.manager.window.showMaximized()
    fig.suptitle(title, fontweight="bold")
    # show
    if not generate_gif:
        plt.show()  # plot figure to see resutls; for testing
    return fig


# fetch real data set
dataset = pd.read_csv(getTimeSeriesDatasetsPath() + getRealDatasetName() + ".csv", sep=',')
dataset['to_timestamp'] = dataset['to_timestamp'].astype('datetime64[ns]')
dataset = dataset[dataset['to_timestamp'].apply(validate_timestamp, date = datetime.datetime(2018, 10, 2, 10, 30))]

# data context
dataContext = [ # hardcodeamos los límites de sweden
                BoundingBox(minimun=11.0273686052 , maximun=23.9033785336),
                BoundingBox(minimun=55.3617373725, maximun=69.1062472602),
            ]
# dyclee
dyclee = Dyclee(dataContext = dataContext, relativeSize = params["relativeSize"], speed = params["speed"], lambd = params["lambd"],
                periodicRemovalAt = params["periodicRemovalAt"], periodicUpdateAt = params["periodicUpdateAt"],
                timeWindow = params["timeWindow"], closenessThreshold = params["closenessThreshold"])

tGlobal = 6000 # siguiendo lo del notebook, estoy tomando casi cada media hs
ac = 0 # represents amount of processed elements

folder = getClusteringResultsPath() + getRealDatasetName() + '/' + getDycleeName() + '/' # for saving the prepared resuls
if will_calculate_DBCV:
    resetStorage(folder) 

first = True # first clustering; 'end' picture will be added at the beggining (to understand the loop)

for ind, p in dataset.iterrows():
    if end(p['to_timestamp']): # break; para no seguir, solo quiero ver los insights de las 11 y 16 del dia 2
        print(p, ' ... (the end)')
        break

    if not validate_p(p): # me saco de encima los que estan por fuera de sweden, y no corresponden al dia que quiero analizar
        continue

    ac += 1
    point = [p.latitude, p.longitude] # ahora esta completo el dataset, hay que subsetear
    dyclee.trainOnElement(point)

    if ac % tGlobal == 0:
        if not validate_timestamp(p['to_timestamp'], date = datetime.datetime(2018, 10, 2, 10, 30)):  # para un analisis mas rapido, mostramos solo lo que interesa: a partir de las 11hs
            print(p, ' ... (no pasa por timestamp)')  # pero empezamos con todos los points de ese dia
            continue

        currMicroClusters = dyclee.getClusteringResult()
        currMicroClusters = filter_unwanted_ones(currMicroClusters) # para sacarme de encima los que arruinan el plot
        ts = p["to_timestamp"].isoformat().replace('T', ' ')
        title = "CURRENT TIMESTAMP: " + ts + "\n"
        
        # if DBCV will be calculated, we need to store snapshots results ....
        if will_calculate_DBCV:
            res = prepareResultFrom(currMicroClusters)
            storeTimeSeriesResult({"processedElements": ac, "result": res}, folder) 
        
        # for plotting outside dyclee
        fig = plot_with_map(currMicroClusters, dataContext, title)

        if generate_gif:
            # save snapshot img
            figures_folder = './results/' + results_path
            if first: # reset folder content
                resetFolderContent(figures_folder)
                first = False
            name = ts + '.png'
            fig.savefig(figures_folder + name)
            sleep(1)
            plt.close()

if generate_gif:
    # gif
    plt.gcf().suptitle('THE END', fontsize=20) # to indicate the moment when the gif starts again
    plt.gcf().savefig(figures_folder + "end.png")
    generate_gif(figures_folder, figures_folder)

# algoConfig: for DBCV calc
algoConfig = dyclee.getConfig()

if generate_gif:
    storeAlgoConfig(algoConfig, figures_folder) # to understand gif; 

if will_calculate_DBCV:
    storeAlgoConfig(algoConfig, folder) # FIXME: uncomment to store prepared results in the general folder!