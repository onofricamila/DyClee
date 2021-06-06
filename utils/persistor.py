import json

import numpy as np
import os
from config import getClusteringResultsPath, getDycleeName, getTimeSeriesToyDatasetName
import shutil
import glob

def resetStorage(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)


def resetFolderContent(folder):
    files = glob.glob(folder + '/*')
    for f in files:
        os.remove(f)


def createDirectoryIfNotExists(folder):
    # check if resourcesFolder needs to be created
    if not os.path.exists(folder):
        os.makedirs(folder)


def storeTimeSeriesResult(snapshot, folder):
    createDirectoryIfNotExists(folder)
    processedElements = snapshot.get("processedElements")
    result = snapshot.get("result")
    targetFile = folder + str(processedElements) + '.csv'
    _storeResult(result, targetFile)


def storeNonTimeSeriesResult(result, folder):
    createDirectoryIfNotExists(folder)
    targetFile = folder + 'result' + '.csv'
    _storeResult(result, targetFile)


def _storeResult(result, targetFile):
    np.savetxt(targetFile, result, delimiter=',',)


def storeAlgoConfig(dict, folder):
    createDirectoryIfNotExists(folder)
    file = folder + 'algoConfig.json'
    with open(file, 'w') as outfile:
        json.dump(dict, outfile)

