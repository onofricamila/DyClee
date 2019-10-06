#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 12:02:00 2019

@author: camila
"""
from utils.uClusters.uCluster import uCluster

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

# uc7
d7 = [0.10, 1.40]
uC7 = uCluster(rs, d7)

# uc8
d8 = [0.05, 1.51]
uC8 = uCluster(rs, d8)

# uc9
d9 = [0, 1.60]
uC9 = uCluster(rs, d9)

# uc10
d10 = [-0.05, 1.60]
uC10 = uCluster(rs, d10)


# ----------------------------------------------------------------------------

rs2 = 1

# uc11
d11 = [1, 1]
uC11 = uCluster(rs2, d11)

# uc12
d12 = [-1, -1]
uC12 = uCluster(rs2, d12)


