#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:56:58 2019

@author: camila
"""

from stage1 import Stage1
from stage2 import Stage2
from multiprocessing import Process, Queue

# s1 to s2 communication queue
s1ToS2ComQueue = Queue()  # s1 will write to s2 there

# s2 to s1 communication queue
s2ToS1ComQueue = Queue()  # s2 will write to s1 there

# stages
s1 = Stage1(s1ToS2ComQueue, s2ToS1ComQueue) # default relative size = 1
s2 = Stage2(s1ToS2ComQueue, s2ToS1ComQueue) # default uncommon dimensions = 0

dataset = [[10, 20]]

s1.formUcs(dataset) # send dataset to s1

# start s2
s2p = Process(target=s2.start(), args=())
s2p.daemon = True
s2p.start()     # launch the stage2 process


s2p.join()   # wait till the stage2 process finishes
    


