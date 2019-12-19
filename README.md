
---

# :hammer::nut_and_bolt: UNDER MAINTENANCE :nut_and_bolt::hammer:

---

# A simple implementation of DyClee in Python

DyClee is a novel algorithm for clustering non-stationary data streams which is currently present in the literature but hasn't yet been implemented.

DyClee's paper can be found [here](https://www.sciencedirect.com/science/article/abs/pii/S0031320319301992) and the software is said to be available [here](https://homepages.laas.fr/louise/drupal/node/36) soon.

Note that this implementation only takes a few possible configurations into account, due to the fact the others go beyond the scope of my personal project.

The subset of parameters that can be passed to the algorithm are listed below:
* relative size
* tGlobal
* uncommon dimensions (uncdim)

Also consider the global approach is used in the density-based stage. 


### :small_orange_diamond: Achieved goals
* As there are many representatives for every cluster, **it is possible to generate non convex groups.** 
* **Noise is handled**: outlier elements will belong to outlier micro clusters
* As every element of the provided dataset is processed once, the algorithm is **perfect for working with streams**. Note that if you wanna use DyClee for clustering a fixed size data set, you will have to set *'tGlobal'* to a value higher than the data set size.
* It's possible to track **evolving environments**. There is no need to specify a fixed number of clusters to be generated. 

If you wanna achieve some other goals, like being able to work with different densities as mentioned in the original paper, feel free to take this implementation as a base :blush:


### :small_orange_diamond: How to try it
The `requirements.txt` file provides the needed packages to run the software. 

Then, as for the algorithm itself, the `config.py` file is the one in which you have to define the dataset you want to use and configure the parameters to be passed to stage 1 and stage 2. Then, just run the `main.py` file and you will see the results :sparkles: 

### :small_orange_diamond: How it works
First of all, there are 2 independent stages that work at different rates:
1. a distance-based one, which job will be to process every element of a given dataset and form the so called __micro clusters__, sending the current ones to the second stage every *'tGlobal'* proccessed samples
2. a density-based one, which constantly receives the micro clusters generated previously and joins them to form the __final groups__, showing them to the user when finished. Every *'tGlobal'* proccessed samples, the user will see plots showing:
    * current clustering, in which every micro cluster centroid is plotted, colored according to the label assigned
    * dense micro clusters evolution taking into account the previous state
    * micro clusters real size, being able to picture the dataset elements assigned to each micro cluster
    
The plots for a 2D dataset would look like these:
![Figure_2](https://user-images.githubusercontent.com/26676136/67420367-de07b700-f5a4-11e9-8fa5-05adb6e1c96a.png)

:bulb: Keep in mind that micro clusters acompass elements which are close according to the *'relative size'* parameter, taking into account all the features. On the other hand, final clusters are a set of connected micro clusters: a chain of dense micro clusters which are directly connected; that meaning micro clusters that are close according to the *'relative size'* parameter, but only in a subset of features (at least total features - *'uncdim'*). Semi dense micro clusters will be at the borders.





