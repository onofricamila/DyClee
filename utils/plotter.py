import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
from utils.helpers.custom_printing_fxs import printInMagenta
import matplotlib
# set matplotlib backend to Qt5Agg to make figure window maximizer work
matplotlib.use('Qt5Agg')

class Plotter:
    def __init__(self, microClusters, dataContext):
        self.densityMedian = 0
        self.densityMean = 0
        self.microClusters = microClusters
        self.dataContext = dataContext


    def calculateDensityMeanAndMedian(self):
        self.densityMean = self.calculateMeanFor(self.microClusters)
        self.densityMedian = self.calculateMedianFor(self.microClusters)


    def calculateMeanFor(self, microClusters):
        return np.mean([microCluster.getD() for microCluster in microClusters])


    def calculateMedianFor(self, microClusters):
        return np.median([microCluster.getD() for microCluster in microClusters])


    def isDense(self, microCluster):
        return (microCluster.getD() >= self.densityMean and microCluster.getD() >= self.densityMedian)


    def isSemiDense(self, microCluster):
        # xor
        return (microCluster.getD() >= self.densityMean) != (microCluster.getD() >= self.densityMedian)


    def isOutlier(self, microCluster):
        return (microCluster.getD() < self.densityMean and microCluster.getD() < self.densityMedian)


    def findDenseMicroClusters(self):
        # it's unnecessary to look for dense microClusters in the oList
        return [microCluster for microCluster in self.microClusters if self.isDense(microCluster) or self.isSemiDense(microCluster)]
        # FIXME: SOLO DENSE?


    def plotClusters(self):
        DMC = self.findDenseMicroClusters()
        if not self.plottableMicroClusters(self.microClusters):
            return
        # let's plot!
        f, (ax1, ax2, ax3,) = plt.subplots(1, 3, sharey=True)  # creates a figure with one row and two columns
        self.plotCurrentClustering(ax1)
        self.plotMicroClustersEvolution(ax2, DMC)
        self.plotMicroClustersSize(ax3)
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


    def plotCurrentClustering(self, ax1):
        # first set markers size to represent different densities
        s = self.getMarkersSizeList(self.microClusters)
        # then get a list with u cluster labels
        labels = [microCluster.label for microCluster in self.microClusters]
        # clusters will be a sequence of numbers (cluster number or -1) for each point in the dataset
        labelsAsNpArray = np.array(labels)
        # get microClusters centroids
        centroids = [microCluster.getCentroid() for microCluster in self.microClusters]
        x, y = zip(*centroids)
        # show info to user
        self.showClusteringInfo(labelsPerUCluster=labels, clusters=labelsAsNpArray, x=x, y=y)
        # scatter'
        ax1.scatter(x, y, c=labelsAsNpArray, cmap="nipy_spectral", marker='s', alpha=0.8, s=s)
        # add general style to subplot n°1
        self.addStyleToSubplot(ax1,
                               title='CURRENT STATE\nlrg square = dense microcluster \nmed square = semidense microcluster\nsml square = outlier microcluster')


    def plotMicroClustersEvolution(self, ax2, DMC):
        (DMCwPrevState, newDMC) = self.formMicroClustersEvolutionLists(DMC)
        for denseMicroClusterWPrevSt in DMCwPrevState:
            # an arrow will be drawn to represent the evolution in the centroid location for a dense micro cluster
            ax2.annotate("", xy=denseMicroClusterWPrevSt.previousCentroid, xytext=denseMicroClusterWPrevSt.getCentroid(),
                         arrowprops=dict(arrowstyle='<-'))
        # get newDMC centroids
        if len(newDMC) is not 0:
            centroids = [microCluster.getCentroid() for microCluster in newDMC]
            x, y = zip(*centroids)
            ax2.plot(x, y, ".", alpha=0.5, )
        # add general style to subplot n°2
        self.addStyleToSubplot(ax2, title='DENSE MICRO CLUSTERS EVOLUTION\n"." means no change \n"->" implies evolution')


    def plotMicroClustersSize(self, ax3):
        # choose palette
        ns = plt.get_cmap('nipy_spectral')
        # get labels
        labels = [microCluster.label for microCluster in self.microClusters]
        # skip repeated leabels
        s = set(labels)
        # especify normalization to get the correct colors
        norm = clrs.Normalize(vmin=min(s), vmax=max(s))
        # for every micro cluster
        for microCluster in self.microClusters:
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
            if (len(denseMicroCluster.previousCentroid) is 0) or (
                    denseMicroCluster.getCentroid() == denseMicroCluster.previousCentroid):
                # dense microCluster hasn't previous state --> is a new dense microCluster
                # dense microCluster prev state and current centroid match --> dense microCluster hasn't changed nor evolutioned; just mark its position
                newDMC.append(denseMicroCluster)
            else:
                # dense microCluster has previous state --> dense microCluster has evolutioned
                DMCwPrevState.append(denseMicroCluster)
        return (DMCwPrevState, newDMC)


    def updateMicroClustersPrevCentroid(self, microClusters, DMC):
        for microCluster in microClusters:
            if microCluster not in DMC:
                # microCluster prev state doesn't matter; if a dense microCluster ended up being an outlier, its position is no longer important
                microCluster.previousCentroid = []
            else:
                # microCluster is dense; current state must be saved for viewing future evolution
                microCluster.previousCentroid = microCluster.getCentroid()


    def addStyleToSubplot(self, ax, title=''):
        # set title
        ax.set_title(title)
        # set axes limits
        xDataContext = self.dataContext[0]
        yDataContext = self.dataContext[1]
        minAndMaxX = [xDataContext.minimun, xDataContext.maximun]  # [54, 64]
        minAndMaxY = [yDataContext.minimun - 1, yDataContext.maximun]  # [10, 20]
        ax.set_xlim(minAndMaxX)
        ax.set_ylim(minAndMaxY)
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
            print("UNABLE TO PLOT CLUSTERS: there are no micro clusters")
            return False
        firstEl = microClusters[0]
        if len(firstEl.CF.LS) != 2:
            print("UNABLE TO PLOT CLUSTERS: it's not a 2D data set")
            return False
        # microClusters are plottable
        return True