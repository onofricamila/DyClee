#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datasets.simpleDatasets import dsChoosingClosestReachableUc, dsForming2uCs, dsFromUcToNoise, dsPilot
from datasets.sklearnDatasets import noisyCirclesDataset, noisyMoonsDataset, blobsDataset
from datasets.customCircunferencesDataset import customCircunferencesDataset
from utils.helpers.custom_printing_fxs import printInGreen

# config

chosenDataset = blobsDataset

rs = 0.06

tG = 100

uncdim = 0

# print info regarding current config

printInGreen("The chosen dataset has " + len(chosenDataset).__repr__() + " elements")

printInGreen("About to cluster data with params: rs -> "  \
             + rs.__repr__() + " , tGlobal -> "  \
             + tG.__repr__() + " , uncdim -> "  \
             + uncdim.__repr__() + " ...")
