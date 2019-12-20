import json

paths = None
algoNames = None
timeSeriesToyDatasetName = None

def _getPaths():
    return paths


def _getAlgoNames():
    return algoNames


def _getTimeSeriesToyDatasetName():
    return timeSeriesToyDatasetName


def _fetchConfig():
    # we use the global key word to being able to change the values of the variables declared outside the function
    global paths
    global algoNames
    global timeSeriesToyDatasetName

    configFilePath = "/home/camila/Desktop/TESIS/DATA/config.json"
    with open(configFilePath) as f:
        data = json.load(f)
    # fill variables
    paths = data.get("paths")
    algoNames = data.get("algoNames")
    timeSeriesToyDatasetName = data.get("timeSeriesToyDatasetName")


def _fetchElementIfNull(_getter):
    element = _getter()
    if (element != None):
        return element
    # else
    _fetchConfig()
    return _getter()


def _getElementFromDict(key, _getter):
    dict = _fetchElementIfNull(_getter)
    return dict.get(key)


def getClusteringResultsPath():
    return _getElementFromDict(key="clusteringResultsPath", _getter=_getPaths)


def getTimeSeriesToyDatasetName():
    return _fetchElementIfNull(_getTimeSeriesToyDatasetName)


def getTimeSeriesDatasetsPath():
    return _getElementFromDict(key="timeSeriesDatasetsPath", _getter=_getPaths)


def getDycleeName():
    return _getElementFromDict(key="dyclee", _getter=_getAlgoNames)


