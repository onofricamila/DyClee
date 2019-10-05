# A simple implementation of DyClee in Python

DyClee is a novel algorithm for clustering non-stationary data streams which is currently present in the literature but hasn't yet been implemented.

DyClee's paper can be found [here](https://www.sciencedirect.com/science/article/abs/pii/S0031320319301992) and the software is said to be available [here](https://homepages.laas.fr/louise/drupal/node/36) soon.

Note that this implementation only takes a few possible configurations into account, due to the fact the others go beyond the scope of the author personal project.

The subset of parameters that can be passed to the algorithm are listed below:
* relative size
* t global
* uncommon dimensions

Consider the global approach is used in the density-based stage. 

### :small_orange_diamond: How it works
First of all, there are 2 independent stages that work at different rates:
1. a distance-based one, which processes every element of a given dataset, creates the so called __micro clusters__, and every 'tGlobal' samples sends them to the second stage
2. a density-based one, which receives the micro clusters generated previously and joins them to form the final groups, eventually showing them to the user

:bulb: Keep in mind that micro clusters acompass elements which are close according to the 'relative size' parameter, and the final clusters are a set of connected micro clusters: a chain of dense micro clusters which are directly connected <taking into account the 'relative size' parameter for (dataset features - 'uncommon dimensions') features>, with semi dense ones in the borders.

Side note: as there are many representatives for every cluster, it is possible to generate non convex groups. 

### :small_orange_diamond: How to try it
The `parametersConfiguration` file is the one in which you have to define the dataset you want to use and configure the parameters to be passed to stage 1 and stage 2. Then, just run the `main` file and you will see the results :blush:



