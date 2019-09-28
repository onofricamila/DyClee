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

# uc6
d6 = [0.15, 1]
uC6 = uCluster(rs, d6)



# TESTING IS DIRECTECTLY CONNECTED U CLUSTER METHOD --> all tests passed :)
# TEST 1°: uC2 llega a ser directly conn con uC1
print(uC1.isDirectlyConnectedWith(uC2, 0)) # --> true

# TEST 2°: uC3 por 1 en ambas dimensiones llega a ser directly conn con uC1
print(uC1.isDirectlyConnectedWith(uC3, 0)) # --> true

# TEST 3°: uC4 por 1 en ambas dimensiones no llega a ser directly conn con uC1
print(uC1.isDirectlyConnectedWith(uC4, 0)) # --> false

# TEST 4°: uC5 es re lejano a uC1
print(uC1.isDirectlyConnectedWith(uC5, 0)) # --> false

# TEST 4°: uC6 no llega a ser directly conn con uC1 por lo que vale la dim 2
print(uC1.isDirectlyConnectedWith(uC6, 0)) # --> false



# TESTING FORM CLUSTERS S2 METHOD --> 
s2 = Stage2(s1ToS2ComQueue, s2ToS1ComQueue)

aL1 = [uC1, uC2, uC4]
oL1 = []
uL1 = [aL1, oL1] 

# TEST 1°: 3 u clusters forman un cluster final por transicion: uc1 -> uc2 -> 4 
s2.formClusters(uL1) # --> :)

