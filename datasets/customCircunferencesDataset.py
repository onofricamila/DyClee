#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import pi, cos, sin, radians
import random

# config ------------------------------------------------------------------------------------------
# circumference properties
h = 0
k = 0
ratio = 1
maxRatioInc = 0.5
ratioPortionForCenterPoints = 10 / 100 * ratio
# batch represents the amount of points to generate per list at a given angle
# we will have 180 * batch points in each list
pointsPerAngle = 5
# pointsPerListToAppend represents the amount of points from a list to be added one next to the other to the dataset
pointsPerListToAppendToDataset = 100



# dataset formation ------------------------------------------------------------------------------------------
# the idea is to get an angle and then use the circunference geometric interpretation and trigonometry to generate points
# on it
def point(theta):
    # increase a little bit the radio [or not]
    r = ratio + random.uniform(0, maxRatioInc)
    # increase or decrease theta (angle)
    theta = theta + random.uniform(0, radians(1)) - random.uniform(0, 0.5)
    # cos(theta) * r --> difference between the point x coordinate and the circumference center one (h)
    # sin(theta) * r --> difference between the point y coordinate and the circumference center one (y)
    return [h + cos(theta) * r, k + sin(theta) * r]



def generatePoints():
    # points lists
    upperPoints = []
    lowerPoints = []
    centerPoints = []

    # theta represents the angle with respect to the x axis from which we will rotate around the circumference center
    for theta in range(0, 180):
        for i in range(0, pointsPerAngle):
          # to generate the upper points we move from right to left (from 0° to 180°)
          upperPoints.append(point(radians(theta)))
          # to generate the lower points we move from left to right (from 180° to 360°)
          lowerPoints.append(point(pi + radians(theta)))
          # to generate the center points we move from right to left but considering a small portion of the original ratio
          # centerPoints.append(point(h, k, centerPointsR, maxRadioInc, radians(theta)))
    return upperPoints, centerPoints, lowerPoints



def generateDataset():
    upperPoints, centerPoints, lowerPoints = generatePoints()
    # parameters regarding the points batchs per list formation
    batchUpperLimit = 0
    batchLowerLimit = 0
    limIterator = len(upperPoints)
    res = []
    for i in range(0, limIterator):
        # increment the batchUpperLimit
        batchUpperLimit += pointsPerListToAppendToDataset
        # select points batches from every list
        res = res \
              + upperPoints[batchLowerLimit:batchUpperLimit] \
              + centerPoints[batchLowerLimit:batchUpperLimit] \
              + lowerPoints[batchLowerLimit:batchUpperLimit]
        # now make batchLowerLimit equal to batchUpperLimit
        batchLowerLimit = batchUpperLimit
    return res



customCircunferencesDataset = generateDataset()
