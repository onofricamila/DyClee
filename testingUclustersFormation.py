#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 12:54:58 2019

@author: camila
"""

from uCluster import uCluster
from stage2 import Stage2
from multiprocessing import Process, Queue

s1ToS2ComQueue = Queue()  # s1 will write to s2 there
s2ToS1ComQueue = Queue()  # s2 will write to s1 there

rs = 0.06 # --> s = 0.06 * {2 - (-2)} = 0.06 * 4 = 0.24
# --> hyperbox size per feature = 0.24 / 2 = 0.12


# uc1
d1 = [0.25, 1.25]
uC1 = uCluster(rs, d1)

# uc2
d2 = [0.15, 1.35]
uC2 = uCluster(rs, d2)

# uc3
d3 = [0.36, 1.14]
uC3 = uCluster(rs, d3)

# uc4
d4 = [0.13, 1.37]
uC4 = uCluster(rs, d4)

# uc5
d5 = [0, 1]
uC5 = uCluster(rs, d5)


# TEST 1°
print(uC1.isDirectlyConnectedWith(uC2, 0)) # --> true

# TEST 2°
print(uC1.isDirectlyConnectedWith(uC3, 0)) # --> true

# TEST 3°
print(uC1.isDirectlyConnectedWith(uC4, 0)) # --> false

# TEST 4°
print(uC1.isDirectlyConnectedWith(uC5, 0)) # --> false










#aL = [uC1, ]
#oL = []
#uL = [aL, oL] 
#
## stages
#s2 = Stage2(s1ToS2ComQueue, s2ToS1ComQueue, uncommonDimensions=0) # default uncommon dimensions = 0
#
#s2.formClusters(uL)