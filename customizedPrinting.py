#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 14:37:00 2019

@author: camila
"""
from termcolor import colored


def printInBlueForDebugging(msg):
  printInBold(msg, 'blue')
  
  
  
def printInMagentaForDebugging(msg):
  printInBold(msg, 'magenta')
  
  
  
def printInBold(msg, color):
  print(colored(msg, color, attrs=['bold']))