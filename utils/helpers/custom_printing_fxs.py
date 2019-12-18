#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from termcolor import colored

def printInBlue(msg):
  printInBold(msg, 'cyan')


def printInMagenta(msg):
  printInBold(msg, 'magenta')


def printInGreen(msg):
  printInBold(msg, 'green')


def printInBold(msg, color):
  print(colored(msg, color, attrs=['bold']))