#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:56:58 2019

@author: camila
"""

from stage1 import Stage1
from stage2 import Stage2
from multiprocessing import Process, Queue
from datasets import dsPilot, dsForming2uCs, dsChoosingClosestReachableUc, dsFromUcToNoise
from datasets import noisyCirclesDataset
from datasets import noisyMoonsDataset
from datasets import blobsDataset

# s1 to s2 communication queue
s1ToS2ComQueue = Queue()  # s1 will write to s2 there

# s2 to s1 communication queue
s2ToS1ComQueue = Queue()  # s2 will write to s1 there

# chosen dataset
dataset = noisyMoonsDataset

# stages
s1 = Stage1(s1ToS2ComQueue, s2ToS1ComQueue, relativeSize=0.06, tGlobal=1500) # default relative size = 1
s2 = Stage2(s1ToS2ComQueue, s2ToS1ComQueue, uncommonDimensions=0) # default uncommon dimensions = 0

# start s1
s1p = Process(target=s1.start, args=(dataset,))
s1p.daemon = True
s1p.start()     # launch the stage1 process

# start s2
s2p = Process(target=s2.start, args=())
s2p.daemon = True
s2p.start()     # launch the stage2 process
    
s1p.join()   # wait till the stage1 process finishes
s2p.join()   # wait till the stage2 process finishes


