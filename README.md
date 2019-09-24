# A simple implementation of DyClee in Python

DyClee is a novel algorithm for clustering non-stationary data streams which is currently present in the literature but hasn't yet been implemented.

DyClee's paper can be found [here](https://www.sciencedirect.com/science/article/abs/pii/S0031320319301992) and the software is said to be available [here](https://homepages.laas.fr/louise/drupal/node/36) soon.

Note that this implementation only takes a few possible configurations into account, due to the fact the others go beyond the scope of the author personal project.

The subset of parameters that can be passed to the algorithm are listed below:
* relative size
* t global
* uncommon dimensions

Finally, the global approach is used in the density-based stage. 


