# A simple implementation of DyClee in Python

DyClee is a novel algorithm for clustering non-stationary data streams which is currently present in the literature but hasn't yet been implemented.

DyClee's paper can be found [here](https://www.sciencedirect.com/science/article/abs/pii/S0031320319301992) and the software is said to be available [here](https://homepages.laas.fr/louise/drupal/node/36) soon.

Note that this implementation only takes a few possible configurations into account, due to the fact the others go beyond the scope of the author personal project.

The subset of parameters that can be passed to the algorithm are listed below:
* relative size
* t global
* uncommon dimensions

Consider the global approach is used in the density-based stage. 

### How does it work
First of all, there are 2 independent stages that work at different rates:
1. a distance-based one, which processes every element of a given dataset, creates the so called __micro clusters__, and every 'tGlobal' samples sends them to the second stage
2. a density-based one, which receives the micro clusters generated previously and joins them to form the final groups,  showing them to the user

--> Keep in mind that micro clusters acommpass elements which are close according to the 'relative size' parameter, and the final clusters are a set of micro clusters connected: a chain of directly connected dense micro clusters <taking into account the 'relative size' parameter for (dataset features - 'uncommon dimensions')>, with semi dense ones in the borders.

Finally, as there are many representatives for every cluster, it is possible to generate non convex groups. 

### How to try it
The 'main' file is the one in which you have to assign the dataset you want and configure the parameters to be passed to stage 1 and stage 2. Just run it and you will see the results :)



