#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 15:16:31 2019

@author: camila
"""

class BoundingBox:

    def __init__(self, minimun, maximun):
        self.minimun = minimun
        self.maximun = maximun
        
        
    
    def __repr__(self):
     return f'\n\t\t BoundingBox =>\n\t\t\tminimun: {self.minimun},\n\t\t\tmaximun: {self.maximun}'