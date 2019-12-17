# S1
from utils.uClusters.uCluster import uCluster
from utils.helpers.customPrintingFxs import printInBlue
from utils.helpers.customMathFxs import stddev
# S2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
from utils.helpers.customPrintingFxs import printInMagenta
import matplotlib
# set matplotlib backend to Qt5Agg to make figure window maximizer work
matplotlib.use('Qt5Agg')

class Dyclee:
    def __init__(self, relativeSize=1, tGlobal=1, uncommonDimensions = 0, initPoints = 100):
        # stage1 algo instance variables
        self.relativeSize = relativeSize
        self.tGlobal = tGlobal
        self.aList = []
        self.oList = []
        self.processedElements = 0
        self.timestamp = 0
        # to be calculated when the dataset is received
        self.meanList = []
        self.SDList = []
        # stage2 algo instance variables
        self.densityMean = 0
        self.densityMedian = 0
        self.uncommonDimensions = uncommonDimensions

    # main method
    # def start(self, dataset):
    #     self.calculateMeanAndSD(dataset)
    #     scaledDataset = self.scaleDataset(dataset)
    #     self.formUcs(scaledDataset)
    #
    # def scaleDataset(self, dataset):
    #     res = []
    #     # for each element
    #     for i in range(len(dataset)):
    #         scaledEl = self.scaleDatasetElement(dataset[i])
    #         res.append(scaledEl)
    #     return res
    #
    # def scaleDatasetElement(self, el):
    #     scaledEl = []
    #     # for each dimension
    #     for fIndex in range(len(el)):
    #         fValue = el[fIndex]
    #         scaledFeature = self.scaleDatasetElementFeature(fValue, fIndex)
    #         scaledEl.append(scaledFeature)
    #     return scaledEl
    #
    # def scaleDatasetElementFeature(self, fValue, fIndex):
    #     return (fValue - self.meanList[fIndex]) / self.SDList[fIndex]


    def trainOnElement(self, newEl):
        self.processedElements += 1
        # TODO: check if a param like denstream speed is needed ... now, time stamp increments every time
        self.timestamp += 1
        # TODO: new instance?
        self.formUcs(self.initBuffer)





    def formUcs(self, dataset):
        # ASSUMPTIONS: dataset es un vector de vectores
        for d in dataset:
            # processed_elements ++
            # self.processedElements += 1 # done in train on el
            # find reachable u clusters for the new element
            reachableUcs = self.findReachableUcs(d)
            if not reachableUcs:
                # empty list -> create u cluster from element
                # the uC will have the parametrized relative size
                uC = uCluster(self.relativeSize, d)
                self.oList.append(uC)
            else:
                # find closest reachable u cluster
                closestUc = self.findClosestReachableUc(d, reachableUcs)
                closestUc.addElement(d)
            # self self.aList, self.oList are updated


    #
    # def calculateMeanAndSD(self, dataset):
    #     n = len(dataset)
    #     # sample taken to get the ammount of features
    #     anElement = dataset[0]
    #     # for each feature
    #     for fIndex in range(len(anElement)):
    #         acPerFeature = 0
    #         fValuesList = []
    #         # for each element in dataset
    #         for i in range(n):
    #             el = dataset[i]
    #             fValue = el[fIndex]
    #             acPerFeature += fValue
    #             # to later obtain ssdev
    #             fValuesList.append(fValue)
    #         featureMean = acPerFeature / n
    #         self.meanList.append(featureMean)
    #         featureSD = stddev(data=fValuesList, mean=featureMean)
    #         self.SDList.append(featureSD)

    # checks if there's a msg from s2 so both u cluster lists must be updated
    def checkUpdatedListsFromStage2(self):
        printInBlue("S1 waiting for lists from s2")
        lists = self.s2ToS1ComQueue.get()
        aList, oList = lists
        # update both lists
        self.aList = aList
        self.oList = oList

        # returns a list of reachable u clusters for a given element

    def findReachableUcs(self, d):
        reachableUcs = self.getReachableUcsFrom(self.aList, d)
        if not reachableUcs:
            # empty list -> check oList
            reachableUcs = self.getReachableUcsFrom(self.oList, d)
        return reachableUcs

    # modifies reareachableUcs iterating over a given list of u clusters
    def getReachableUcsFrom(self, uCsList, d):
        res = []
        for uC in uCsList:
            # the uC has the parametrized relative size
            if uC.isReachableFrom(d):
                res.append(uC)
        return res

        # returns the closest uC for an element, given a set of reachable uCs

    def findClosestReachableUc(self, d, reachableUcs):
        closestUc = None
        minDistance = float("inf")
        for uC in reachableUcs:
            distance = self.manhatanDistance(d, uC)
            if distance < minDistance:
                minDistance = distance
                closestUc = uC
        return closestUc

    # returns the manhatan distance between a cluster and an element
    def manhatanDistance(self, d, uC):
        dist = 0
        uCCentroid = uC.getCentroid()
        # for every feature/dimension
        for i in range(len(d)):
            diff = d[i] - uCCentroid[i]
            dist = dist + abs(diff)
        return dist

    # returns true if it's time to send message to stage 2
    def timeToSendMessage(self):
        return self.processedElements == self.tGlobal

    def sendListsToStage2(self):
        self.s1ToS2ComQueue.put((self.aList, self.oList))

    def resetProcessedElements(self):
        self.processedElements = 0

    def sendEndMsgToStage2(self):
        self.s1ToS2ComQueue.put("DONE")



# S2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!


def start(self):
    while True:
        # wait for lists from s1
        msg = self.s1ToS2ComQueue.get()
        if msg == "DONE":
            break
        # uC lists were received
        lists = msg
        # update mean and median
        self.updateMeanAndMedian(lists)
        # update lists according to uC density
        updatedLists = self.updateLists(lists)
        # extract active and outlier uCs
        updatedAList, updatedOList = updatedLists
        # get both active and outlier uCs together
        uCs = updatedAList + updatedOList
        # extract dense uCs from active list (it's unnecessary to look for dense uCs in the oList)
        DMC = self.findDenseUcs(updatedAList)
        # form final clusters
        self.formClusters(updatedAList=updatedAList, updatedOList=updatedOList, DMC=DMC)
        # plot current state and micro cluster evolution
        self.plotClusters(uCs, DMC)
        # update prev state once the evolution was plotted
        self.updateUcsPrevState(uCs, DMC)
        # send updated uCs lists to s1 (needs to be done at this point to make prev state last; labels will last too)
        self.s2ToS1ComQueue.put(updatedLists)


def updateLists(self, lists):
    aList, oList = lists
    newAList = []
    newOList = []
    concatenatedLists = aList + oList
    for uC in concatenatedLists:
        if self.isOutlier(uC):
            newOList.append(uC)
        else:
            # uC is dense or semi dense
            newAList.append(uC)
    return (newAList, newOList)


def updateMeanAndMedian(self, lists):
    aList, oList = lists
    concatenatedLists = aList + oList
    self.densityMean = self.calculateMeanFor(concatenatedLists)
    self.densityMedian = self.calculateMedianFor(concatenatedLists)


def resetLabelsAsUnclass(self, uCs):
    for uC in uCs:
        uC.label = -1


def calculateMeanFor(self, uCs):
    return np.mean([uC.CF.D for uC in uCs])


def calculateMedianFor(self, uCs):
    return np.median([uC.CF.D for uC in uCs])

    # returns true if a given u cluster is considered dense


def isDense(self, uC):
    return (uC.CF.D >= self.densityMean and uC.CF.D >= self.densityMedian)

    # returns true if a given u cluster is considered semi dense


def isSemiDense(self, uC):
    # xor
    return (uC.CF.D >= self.densityMean) != (uC.CF.D >= self.densityMedian)

    # returns true if a given u cluster is considered outlier


def isOutlier(self, uC):
    return (uC.CF.D < self.densityMean and uC.CF.D < self.densityMedian)

    # returns only dense u clusters from a set of u clusters


def findDenseUcs(self, uCs):
    return [uC for uC in uCs if self.isDense(uC)]


def findDirectlyConnectedUcsFor(self, uC, uCs):
    res = []
    for u in uCs:
        if uC.isDirectlyConnectedWith(u, self.uncommonDimensions):
            res.append(u)
    return res


def formClusters(self, updatedAList, updatedOList, DMC):
    # init currentClusterId
    currentClusterId = 0
    # reset uCs labels as -1
    self.resetLabelsAsUnclass(updatedAList)
    self.resetLabelsAsUnclass(updatedOList)
    # start clustering
    alreadySeen = []
    for denseUc in DMC:
        if denseUc not in alreadySeen:
            alreadySeen.append(denseUc)
            currentClusterId += 1
            denseUc.label = currentClusterId
            connectedUcs = self.findDirectlyConnectedUcsFor(denseUc, updatedAList)
            self.growCluster(currentClusterId, alreadySeen, connectedUcs, updatedAList)
    # for loop finished -> clusters were formed


def growCluster(self, currentClusterId, alreadySeen, connectedUcs, uCs):
    i = 0
    while i < len(connectedUcs):
        conUc = connectedUcs[i]
        if (conUc not in alreadySeen):
            conUc.label = currentClusterId
            alreadySeen.append(conUc)
            if self.isDense(conUc):
                newConnectedUcs = self.findDirectlyConnectedUcsFor(conUc, uCs)
                for newNeighbour in newConnectedUcs:
                    connectedUcs.append(newNeighbour)
        i += 1


def plotClusters(self, uCs, DMC):
    f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)  # creates a figure with one row and two columns
    self.plotCurrentClustering(ax1, uCs)
    self.plotMicroClustersEvolution(ax2, DMC)
    self.plotMicroClustersSize(ax3, uCs)
    # show both subplots
    f.canvas.manager.window.showMaximized()
    plt.show()


def getMarkersSizeList(self, uCs):
    res = []
    for uC in uCs:
        if self.isOutlier(uC):
            # really small size -> comes out almost as a point
            res.append(5)
        elif self.isSemiDense(uC):
            # big marker
            res.append(20)
        elif self.isDense(uC):
            # medium size marker
            res.append(50)
    return res


def plotCurrentClustering(self, ax1, uCs):
    if not self.plottableUcs(uCs):
        return
    # let's plot!
    # first set markers size to represent different densities
    s = self.getMarkersSizeList(uCs)
    # then get a list with u cluster labels
    labelsPerUCluster = [uC.label for uC in uCs]
    # clusters will be a sequence of numbers (cluster number or -1) for each point in the dataset
    clusters = np.array(labelsPerUCluster)
    # get uCs centroids
    centroids = [uC.getCentroid() for uC in uCs]
    x, y = zip(*centroids)
    # show info to user
    self.showClusteringInfo(labelsPerUCluster=labelsPerUCluster, clusters=clusters, x=x, y=y)
    # scatter'
    ax1.scatter(x, y, c=clusters, cmap="nipy_spectral", marker='s', alpha=0.8, s=s)
    # add general style to subplot n°1
    self.addStyleToSubplot(ax1,
                           title='CURRENT STATE\nlrg square = dense microcluster \nmed square = semidense microcluster\nsml square = outlier microcluster')


def plotMicroClustersEvolution(self, ax2, DMC):
    (DMCwPrevState, newDMC) = self.formMicroClustersEvolutionLists(DMC)
    for denseUcWPrevSt in DMCwPrevState:
        ax2.annotate("", xy=denseUcWPrevSt.previousState, xytext=denseUcWPrevSt.centroid,
                     arrowprops=dict(arrowstyle='<-'))
    # get newDMC centroids
    if len(newDMC) is not 0:
        centroids = [uC.centroid for uC in newDMC]
        x, y = zip(*centroids)
        ax2.plot(x, y, ".", alpha=0.5, )
    # add general style to subplot n°2
    self.addStyleToSubplot(ax2, title='DENSE MICRO CLUSTERS EVOLUTION\n"." means no change \n"->" implies evolution')


def plotMicroClustersSize(self, ax3, uCs):
    # choose palette
    ns = plt.get_cmap('nipy_spectral')
    # get labels
    labelsPerUCluster = [uC.label for uC in uCs]
    # skip repeated leabels
    s = set(labelsPerUCluster)
    # especify normalization to get the correct colors
    norm = clrs.Normalize(vmin=min(s), vmax=max(s))
    # for every micro cluster
    for uC in uCs:
        # get coordinate x from uC centroid
        realX = uC.centroid[0]
        # get coordinate y from uC centroid
        realY = uC.centroid[1]
        # x n y are the bottom left coordinates for the rectangle
        # to obtain them we have to substract half the hyperbox size to both coordinates
        offsetX = uC.hyperboxSizePerFeature[0] / 2
        offsetY = uC.hyperboxSizePerFeature[1] / 2
        x = realX - offsetX
        y = realY - offsetY
        # the following are represented from the bottom left angle coordinates of the rectangle
        width = uC.hyperboxSizePerFeature[0]
        height = uC.hyperboxSizePerFeature[1]
        # get the color
        c = ns(norm(uC.label))
        # make the rectangle
        rect = plt.Rectangle((x, y), width, height, color=c, alpha=0.5)
        ax3.add_patch(rect)
        # plot the rectangle center (uC centroid)
        ax3.plot(realX, realY, ".", color=c, alpha=0.3)
    self.addStyleToSubplot(ax3, title='MICRO CLUSTERS REAL SIZE')


def formMicroClustersEvolutionLists(self, DMC):
    DMCwPrevState = []
    newDMC = []
    for denseUc in DMC:
        if (len(denseUc.previousState) is 0) or (denseUc.centroid == denseUc.previousState):
            # dense uC hasn't previous state --> is a new dense uC
            # dense uC prev state and current centroid match --> dense uC hasn't changed nor evolutioned; just mark its position
            newDMC.append(denseUc)
        else:
            # dense uC has previous state --> dense uC has evolutioned
            DMCwPrevState.append(denseUc)
    return (DMCwPrevState, newDMC)


def updateUcsPrevState(self, uCs, DMC):
    for uC in uCs:
        if uC not in DMC:
            # uC prev state doesn't matter; if a dense uC turned out to be an outlier, its position is no longer important
            uC.previousState = []
        else:
            # uC is dense; current state must be saved for viewing future evolution
            uC.previousState = uC.centroid


def addStyleToSubplot(self, ax, title=''):
    # set title
    ax.set_title(title)
    # set axes limits
    minAndMaxDeviations = [-2.5, 2.5]
    ax.set_xlim(minAndMaxDeviations)
    ax.set_ylim(minAndMaxDeviations)
    # set plot general characteristics
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.grid(color='k', linestyle=':', linewidth=1)


def showClusteringInfo(self, labelsPerUCluster, clusters, x, y):
    # show final clustering info
    dic = self.clustersElCounter(labelsPerUCluster)
    dicLength = len(dic)
    if dicLength == 1:
        msg = "There is only 1 final cluster and "
    else:
        msg = "There are " + len(dic).__repr__() + " final clusters and "
    if -1 in labelsPerUCluster:
        msg += "one of them represents outliers (the black one)."
    else:
        msg += "no outliers."
    printInMagenta(msg + "\n")
    for key, value in dic.items():
        printInMagenta("- Cluster n°" + key.__repr__() + " -> " + value.__repr__() + " uCs" + "\n")
    # show detailed info regarding lists of uCs coordinates and labels
    printInMagenta("* uCs labels: " + '\n' + clusters.__repr__() + '\n')
    printInMagenta("* uCs 'x' coordinates: " + '\n' + x.__repr__() + '\n')
    printInMagenta("* uCs 'y' coordinates: " + '\n' + y.__repr__())

    # returns a dictionary in which every position represents a cluster and every value is the amount of uCs w that label


def clustersElCounter(self, labelsPerUCluster):
    dicKeys = set(labelsPerUCluster)
    dic = {key: 0 for key in dicKeys}
    for c in labelsPerUCluster:
        dic[c] += 1
    return dic

    # returns True if uCs are plottable (regarding amount of features)


def plottableUcs(self, uCs):
    if len(uCs) == 0:
        # there are't any u clusters to plot
        return False
    firstEl = uCs[0]
    if len(firstEl.CF.LS) != 2:
        print("UNABLE TO DRAW CLUSTERS: IT'S NOT A 2D DATASET")
        return False
    # uCs are plottable
    return True