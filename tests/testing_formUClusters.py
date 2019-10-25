#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from testing_uClusters import uC1, uC2, uC3, uC4, uC5, uC6, uC7, uC8, uC9
from utils.stages.stage2 import Stage2
from multiprocessing import Queue
# TODO: consider S/2 while checking if 2 uCs are directly connected ....
s1ToS2ComQueue = Queue()  # s1 will write to s2 there
s2ToS1ComQueue = Queue()  # s2 will write to s1 there

s2 = Stage2(s1ToS2ComQueue, s2ToS1ComQueue)

# uL1
aL1 = [uC1, uC2, uC4]
oL1 = []
uL1 = (aL1, oL1)

# uL2
aL2 = [uC1, uC2, uC3, uC4, uC5, uC6]
oL2 = []
uL2 = (aL2, oL2) 

# uL3
aL3 = [uC1, uC3, uC4, uC5, uC6]
oL3 = [uC2,]
uL3 = (aL3, oL3) 

# uL4
aL4 = [uC1, uC4, uC5, uC6]
oL4 = [uC2, uC3]
uL4 = (aL4, oL4) 

# uL5
aL5 = [uC1, uC3, uC4, uC5, uC6, uC7, uC8, uC9]
oL5 = [uC2]
uL5 = (aL5, oL5) 

# uL6
aL6 = [uC1, uC2, uC3, uC4, uC5, uC6, uC7, uC8, uC9]
oL6 = []
uL6 = (aL6, oL6) 

# TEST 1°: 
# oList vacia
# 3 u clusters forman un cluster final por transicion: uC1 -> uC2 -> uC4 
print('\n', '1) 1 cluster')
s2.formClusters(uL1) # --> 1 cluster :)

# TEST 2°:
# oList vacia
# 6 u clusters forman 3 clusters finales:
# uC1 -> uC2 -> uC4,    uC5,    uC6
#     -> uC3
print('\n', '2) 3 clusters')
s2.formClusters(uL2) # --> 3 clusters :)

# TEST 3°:
# oList con uC2 -> el uC1 no tiene como llegar al 4
# deberian formarse 4 clusters
# uC1 -> uC3,    uC4,    uC5,    uC6
# + uC2 como outlier
print('\n', '3) 4 clusters + 1 noise')
s2.formClusters(uL3) # --> 4 clusters + noise

# TEST 4°:
# oList con uC3 y uC2 -> el uC1 no tiene como llegar al 4
# deberian formarse 4 clusters
# uC1,    uC4,    uC5,    uC6
# + uC2 y uC3 como outliers
print('\n', '4) 4 clusters + 2 noise')
s2.formClusters(uL4) # --> 4 clusters + noise v2

# TEST 5°:
# oList con uC2 -> el uC1 no tiene como llegar al 4
# deberian formarse 4 clusters
# uC1,    uC4 -> uC7 -> uC8 -> uC9,    uC5,    uC6
# + uC2 como outlier
print('\n', '5) 4 clusters + 1 noise')
s2.formClusters(uL5) # --> 4 clusters + noise v3

# TEST 6°:
# oList vacia
# 4 clusters
# uC1 -> uC2 -> uC4 -> uC7 -> uC8 -> uC9,    uC5,    uC6
#     -> uC3
print('\n', '6) 3 clusters')
s2.formClusters(uL6) # --> 

