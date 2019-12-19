# S1
from utils.helpers.custom_math_fxs import manhattanDistance
from utils.micro_clusters.micro_cluster import MicroCluster
from utils.timestamp import Timestamp
from math import log10
# S2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
from utils.helpers.custom_printing_fxs import printInMagenta
import matplotlib
# set matplotlib backend to Qt5Agg to make figure window maximizer work
matplotlib.use('Qt5Agg')


class Dyclee:
    def __init__(self, relativeSize=0.2, speed = 25, uncommonDimensions = 0, lambd = 0.8, periodicRemovalAt = 50, periodicUpdateAt = 50):
        self.relativeSize = relativeSize
        self.processingSpeed = speed
        self.lambd = lambd
        self.tp = periodicRemovalAt
        self.tu = periodicUpdateAt
        self.aList = []
        self.oList = []
        self.processedElements = 0
        self.timestamp = 0
        self.currTimestamp = Timestamp() # initialized at 0
        self.densityMean = 0
        self.densityMedian = 0
        self.uncommonDimensions = uncommonDimensions
        # for normalization; to be calculated when the data set is received
        self.meanValuePerFeature = []
        self.SDPerFeature = []


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

    # returns a list of floats given an iterable object
    def trainOnElement(self, newEl):
        # get an object matching the desired format (to guarantee consistency)
        point = self.getListOfFloatsFromIterable(newEl)
        self.processedElements += 1
        # control the stream speed
        # TODO: check if the "speed" param is ok ...
        if self.timeToIncTimestamp():
            self.timestamp += 1
            self.currTimestamp.timestamp = self.timestamp
        # now, check what to do with the new point
        self.processPoint(point)
        if self.timeToCheckMicroClustersTl():
            self.checkMicroClustersTl()
        # periodic cluster removal
        if self.timePerformPeriodicClusterRemoval():
            self.performPeriodicClusterRemoval()


    def getListOfFloatsFromIterable(self, newEl):
        point = []
        for value in newEl:
            point.append(float(value))
        return point


    def timeToIncTimestamp(self):
        return self.processedElements % self.processingSpeed == 0


    def timePerformPeriodicClusterRemoval(self):
        return self.processedElements % self.tp == 0


    def timeToCheckMicroClustersTl(self):
        return self.processedElements % self.tu == 0


    def processPoint(self, point):
        # ASSUMPTION: point is a list of floats
        # find reachable u clusters for the new element
        reachableMicroClusters = self.findReachableMicroClusters(point)
        if not reachableMicroClusters:
            # empty list -> create u cluster from element
            # the microCluster will have the parametrized relative size, and the Timestamp object to being able to access the
            # current timestamp any atime
            microCluster = MicroCluster(self.relativeSize, self.currTimestamp, point)
            self.oList.append(microCluster)
        else:
            # find closest reachable u cluster
            closestMicroCluster = self.findClosestReachableMicroCluster(point, reachableMicroClusters)
            closestMicroCluster.addElement(point=point, lambd=self.lambd)
        # at this point, self self.aList and self.oList are updated


    def checkMicroClustersTl(self):
        microClusters = self.aList + self.oList
        for micCluster in microClusters:
            if (self.timestamp - micCluster.CF.tl) > self.tu:
                micCluster.applyDecayComponent(self.lambd)


    def performPeriodicClusterRemoval(self):
        # if the density of an outlier micro cluster drops below the low density threshold, it is eliminated
        newOList = []
        for oMicroCluster in self.oList:
            if oMicroCluster.CF.D >= self.getDensityThershold():
                newOList.append(oMicroCluster)
        # at this point micro clusters that do not fulfil the density requirement were discarded
        self.oList = newOList


    def getDensityThershold(self):
        self.calculateDensityMeanAndMedian()
        return self.densityMean * 0.75


    def applyDecayComponent(self):
        for micCluster in self.aList + self.oList:
            if self.timestamp - micCluster.CF.tl > self.tu:
                micCluster.applyDecayComponent(self.lambd)

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


    # returns a list of reachable u clusters for a given element
    def findReachableMicroClusters(self, point):
        reachableMicroClusters = self.getReachableMicroClustersFrom(self.aList, point)
        if not reachableMicroClusters:
            # empty list -> check oList
            reachableMicroClusters = self.getReachableMicroClustersFrom(self.oList, point)
        return reachableMicroClusters


    # modifies reareachableMicroClusters iterating over a given list of u clusters
    def getReachableMicroClustersFrom(self, microClustersList, point):
        res = []
        for microCluster in microClustersList:
            # the microCluster has the parametrized relative size
            if microCluster.isReachableFrom(point):
                res.append(microCluster)
        return res


    # returns the closest microCluster for an element, given a set of reachable microClusters
    def findClosestReachableMicroCluster(self, point, reachableMicroClusters):
        closestMicroCluster = None
        minDistance = float("inf")
        for microCluster in reachableMicroClusters:
            distance = manhattanDistance(point, microCluster.getCentroid())
            if distance < minDistance:
                minDistance = distance
                closestMicroCluster = microCluster
        return closestMicroCluster




# S2 !!!!!!!!!!!!!!!!!!!!!!!!!!!!


    def getClusteringResult(self):
        # update density mean and median values with current ones
        self.calculateDensityMeanAndMedian()
        # rearrange lists according to microClusters density, considering density mean and median limits
        self.rearrangeLists()
        # extract dense microClusters from active list
        DMC = self.findDenseMicroClusters()
        # form final clusters
        self.formClusters(DMC)
        # concatenate them: get both active and outlier microClusters together
        microClusters = self.aList + self.oList
        # plot current state and micro cluster evolution
        if microClusters is not None:
            self.plotClusters(microClusters, DMC)
        # update prev state once the evolution was plotted
        self.updateMicroClustersPrevState(microClusters, DMC)
        # send updated microClusters lists to s1 (needs to be done at this point to make prev state last; labels will last too)
        # TODO: store clustering result -> microClusters


    def rearrangeLists(self,):
        newAList = []
        newOList = []
        concatenatedLists = self.aList + self.oList
        for microCluster in concatenatedLists:
            if self.isOutlier(microCluster):
                newOList.append(microCluster)
            else:
                # microCluster is dense or semi dense
                newAList.append(microCluster)
        self.aList = newAList
        self.oList = newOList


    def calculateDensityMeanAndMedian(self):
        concatenatedLists = self.aList + self.oList
        self.densityMean = self.calculateMeanFor(concatenatedLists)
        self.densityMedian = self.calculateMedianFor(concatenatedLists)


    def resetLabelsAsUnclass(self, microClusters):
        for microCluster in microClusters:
            microCluster.label = -1


    def calculateMeanFor(self, microClusters):
        return np.mean([microCluster.CF.D for microCluster in microClusters])


    def calculateMedianFor(self, microClusters):
        return np.median([microCluster.CF.D for microCluster in microClusters])


    # returns true if a given u cluster is considered dense
    def isDense(self, microCluster):
        return (microCluster.CF.D >= self.densityMean and microCluster.CF.D >= self.densityMedian)


    # returns true if a given u cluster is considered semi dense
    def isSemiDense(self, microCluster):
        # xor
        return (microCluster.CF.D >= self.densityMean) != (microCluster.CF.D >= self.densityMedian)


    # returns true if a given u cluster is considered outlier
    def isOutlier(self, microCluster):
        return (microCluster.CF.D < self.densityMean and microCluster.CF.D < self.densityMedian)


    # returns only dense u clusters from a set of u clusters
    def findDenseMicroClusters(self):
        # it's unnecessary to look for dense microClusters in the oList
        return [microCluster for microCluster in self.aList if self.isDense(microCluster)]


    def findDirectlyConnectedMicroClustersFor(self, microCluster, microClusters):
        res = []
        for u in microClusters:
            if microCluster.isDirectlyConnectedWith(u, self.uncommonDimensions):
                res.append(u)
        return res


    def formClusters(self, DMC):
        # init currentClusterId
        currentClusterId = 0
        # reset microClusters labels as -1
        self.resetLabelsAsUnclass(self.aList)
        self.resetLabelsAsUnclass(self.oList)
        # start clustering
        alreadySeen = []
        for denseMicroCluster in DMC:
            if denseMicroCluster not in alreadySeen:
                alreadySeen.append(denseMicroCluster)
                currentClusterId += 1
                denseMicroCluster.label = currentClusterId
                connectedMicroClusters = self.findDirectlyConnectedMicroClustersFor(denseMicroCluster, self.aList)
                self.growCluster(currentClusterId, alreadySeen, connectedMicroClusters, self.aList)


    # for loop finished -> clusters were formed
    def growCluster(self, currentClusterId, alreadySeen, connectedMicroClusters, microClusters):
        i = 0
        while i < len(connectedMicroClusters):
            conMicroCluster = connectedMicroClusters[i]
            if (conMicroCluster not in alreadySeen):
                conMicroCluster.label = currentClusterId
                alreadySeen.append(conMicroCluster)
                if self.isDense(conMicroCluster):
                    newConnectedMicroClusters = self.findDirectlyConnectedMicroClustersFor(conMicroCluster, microClusters)
                    for newNeighbour in newConnectedMicroClusters:
                        connectedMicroClusters.append(newNeighbour)
            i += 1


    def plotClusters(self, microClusters, DMC):
        f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)  # creates a figure with one row and two columns
        self.plotCurrentClustering(ax1, microClusters)
        self.plotMicroClustersEvolution(ax2, DMC)
        self.plotMicroClustersSize(ax3, microClusters)
        # show both subplots
        f.canvas.manager.window.showMaximized()
        plt.show()


    def getMarkersSizeList(self, microClusters):
        res = []
        for microCluster in microClusters:
            if self.isOutlier(microCluster):
                # really small size -> comes out almost as a point
                res.append(5)
            elif self.isSemiDense(microCluster):
                # big marker
                res.append(20)
            elif self.isDense(microCluster):
                # medium size marker
                res.append(50)
        return res


    def plotCurrentClustering(self, ax1, microClusters):
        if not self.plottableMicroClusters(microClusters):
            return
        # let's plot!
        # first set markers size to represent different densities
        s = self.getMarkersSizeList(microClusters)
        # then get a list with u cluster labels
        labelsPerUCluster = [microCluster.label for microCluster in microClusters]
        # clusters will be a sequence of numbers (cluster number or -1) for each point in the dataset
        clusters = np.array(labelsPerUCluster)
        # get microClusters centroids
        centroids = [microCluster.getCentroid() for microCluster in microClusters]
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
        for denseMicroClusterWPrevSt in DMCwPrevState:
            ax2.annotate("", xy=denseMicroClusterWPrevSt.previousState, xytext=denseMicroClusterWPrevSt.getCentroid(),
                         arrowprops=dict(arrowstyle='<-'))
        # get newDMC centroids
        if len(newDMC) is not 0:
            centroids = [microCluster.getCentroid() for microCluster in newDMC]
            x, y = zip(*centroids)
            ax2.plot(x, y, ".", alpha=0.5, )
        # add general style to subplot n°2
        self.addStyleToSubplot(ax2, title='DENSE MICRO CLUSTERS EVOLUTION\n"." means no change \n"->" implies evolution')


    def plotMicroClustersSize(self, ax3, microClusters):
        # choose palette
        ns = plt.get_cmap('nipy_spectral')
        # get labels
        labelsPerUCluster = [microCluster.label for microCluster in microClusters]
        # skip repeated leabels
        s = set(labelsPerUCluster)
        # especify normalization to get the correct colors
        norm = clrs.Normalize(vmin=min(s), vmax=max(s))
        # for every micro cluster
        for microCluster in microClusters:
            # get coordinate x from microCluster centroid
            realX = microCluster.getCentroid()[0]
            # get coordinate y from microCluster centroid
            realY = microCluster.getCentroid()[1]
            # x n y are the bottom left coordinates for the rectangle
            # to obtain them we have to substract half the hyperbox size to both coordinates
            offsetX = microCluster.hyperboxSizePerFeature[0] / 2
            offsetY = microCluster.hyperboxSizePerFeature[1] / 2
            x = realX - offsetX
            y = realY - offsetY
            # the following are represented from the bottom left angle coordinates of the rectangle
            width = microCluster.hyperboxSizePerFeature[0]
            height = microCluster.hyperboxSizePerFeature[1]
            # get the color
            c = ns(norm(microCluster.label))
            # make the rectangle
            rect = plt.Rectangle((x, y), width, height, color=c, alpha=0.5)
            ax3.add_patch(rect)
            # plot the rectangle center (microCluster centroid)
            ax3.plot(realX, realY, ".", color=c, alpha=0.3)
        self.addStyleToSubplot(ax3, title='MICRO CLUSTERS REAL SIZE')


    def formMicroClustersEvolutionLists(self, DMC):
        DMCwPrevState = []
        newDMC = []
        for denseMicroCluster in DMC:
            if (len(denseMicroCluster.previousState) is 0) or (denseMicroCluster.getCentroid() == denseMicroCluster.previousState):
                # dense microCluster hasn't previous state --> is a new dense microCluster
                # dense microCluster prev state and current centroid match --> dense microCluster hasn't changed nor evolutioned; just mark its position
                newDMC.append(denseMicroCluster)
            else:
                # dense microCluster has previous state --> dense microCluster has evolutioned
                DMCwPrevState.append(denseMicroCluster)
        return (DMCwPrevState, newDMC)


    def updateMicroClustersPrevState(self, microClusters, DMC):
        for microCluster in microClusters:
            if microCluster not in DMC:
                # microCluster prev state doesn't matter; if a dense microCluster turned out to be an outlier, its position is no longer important
                microCluster.previousState = []
            else:
                # microCluster is dense; current state must be saved for viewing future evolution
                microCluster.previousState = microCluster.getCentroid()


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
            printInMagenta("- Cluster n°" + key.__repr__() + " -> " + value.__repr__() + " microClusters" + "\n")
        # show detailed info regarding lists of microClusters coordinates and labels
        printInMagenta("* microClusters labels: " + '\n' + clusters.__repr__() + '\n')
        printInMagenta("* microClusters 'x' coordinates: " + '\n' + x.__repr__() + '\n')
        printInMagenta("* microClusters 'y' coordinates: " + '\n' + y.__repr__())

        # returns a dictionary in which every position represents a cluster and every value is the amount of microClusters w that label


    def clustersElCounter(self, labelsPerUCluster):
        dicKeys = set(labelsPerUCluster)
        dic = {key: 0 for key in dicKeys}
        for c in labelsPerUCluster:
            dic[c] += 1
        return dic

        # returns True if microClusters are plottable (regarding amount of features)


    def plottableMicroClusters(self, microClusters):
        if len(microClusters) == 0:
            # there are't any u clusters to plot
            return False
        firstEl = microClusters[0]
        if len(firstEl.CF.LS) != 2:
            print("UNABLE TO DRAW CLUSTERS: IT'S NOT A 2D DATASET")
            return False
        # microClusters are plottable
        return True