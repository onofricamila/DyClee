from datasets.sklearnDatasets import noisyCirclesDataset, noisyMoonsDataset, blobsDataset
from datasets.customCircunferencesDataset import customCircunferencesDataset
from utils.dyclee import Dyclee
from sklearn.preprocessing import StandardScaler

dc = Dyclee()

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