from datasets.sklearnDatasets import noisyCirclesDataset, noisyMoonsDataset, blobsDataset
from datasets.customCircunferencesDataset import customCircunferencesDataset
from utils.dyclee import Dyclee
from sklearn.preprocessing import StandardScaler

dc = Dyclee(relativeSize=0.06, speed=100, uncommonDimensions=0)

ac = 0 # processed samples

# for the sklearn datasets
scaler = StandardScaler()
dataset = noisyMoonsDataset
tGlobal = len(dataset)

for d in scaler.fit_transform(dataset):
    ac += 1
    dc.trainOnElement(d)
    if ac % tGlobal == 0:
        dc.getClusteringResult()