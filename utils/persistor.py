import json

import numpy as np
import os
from config2 import getClusteringResultsPath, getDycleeName, getTimeSeriesToyDatasetName
import shutil

folder = getClusteringResultsPath() + getTimeSeriesToyDatasetName() + '/' + getDycleeName() + '/'


def resetStorage():
    if os.path.exists(folder):
        shutil.rmtree(folder)


def createDirectoryIfNotExists(folder):
    # check if resourcesFolder needs to be created
    if not os.path.exists(folder):
        os.makedirs(folder)


def storeResult(snapshot):
    createDirectoryIfNotExists(folder)
    processedElements = snapshot.get("processedElements")
    result = snapshot.get("result")
    targetFile = folder + str(processedElements) + '.csv'
    np.savetxt(targetFile, result, delimiter=',',)


def storeAlgoConfig(dict):
    createDirectoryIfNotExists(folder)
    file = folder + 'algoConfig.json'
    with open(file, 'w') as outfile:
        json.dump(dict, outfile)

