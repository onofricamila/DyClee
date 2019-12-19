from datasets.sklearnDatasets import noisyCirclesDataset, noisyMoonsDataset, blobsDataset
from datasets.customCircunferencesDataset import customCircunferencesDataset
from utils.dyclee import Dyclee
from sklearn.preprocessing import StandardScaler

dc = Dyclee(relativeSize=0.1, speed = 25, uncommonDimensions = 0, lambd = 1, periodicRemovalAt = 50, periodicUpdateAt = 25)

ac = 0 # processed samples

# for the sklearn datasets
scaler = StandardScaler()
dataset = noisyMoonsDataset
tGlobal = len(dataset)

# for d in scaler.fit_transform(dataset):
#     ac += 1
#     dc.trainOnElement(d)
#     if ac % tGlobal == 0:
#         dc.getClusteringResult()

tGlobal = 200
for d in customCircunferencesDataset:
    ac += 1
    dc.trainOnElement(d)
    if ac % tGlobal == 0:
        dc.getClusteringResult()