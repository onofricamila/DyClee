#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class BoundingBox:

    def __init__(self, minimun, maximun):
        self.minimun = minimun
        self.maximun = maximun
        
        
    
    def __repr__(self):
     return f'\n\t\t BoundingBox =>\n\t\t\tminimun: {self.minimun},\n\t\t\tmaximun: {self.maximun}'