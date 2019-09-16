#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:56:58 2019

@author: camila
"""

from stage1 import Stage1
from stage2 import Stage2

s1 = Stage1() # default relative size = 1
s2 = Stage2() # default uncommon dimensions = 0

dataset = "vetor of equal-feature vectors"

s1.formUcs(dataset)
s2.start()
