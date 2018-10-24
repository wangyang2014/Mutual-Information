# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:33:55 2018

@author: wangyang
"""
import numpy as np
from minepy import MINE 

class calulationMIC():
    def __init__(self,X,Y):
        self.X = X
        self.Y = Y
        
    def getMIC(self):
        self.X = np.asarray(self.X,dtype='float')
        self.Y = np.asarray(self.Y,dtype='float')
        mine = MINE(alpha=0.6, c=15)
        mine.compute_score(self.X,self.Y)
        return mine

if __name__ == '__main__': 
    X = [1,2,3,4]
    Y = [1,2,3,5]
    MI = calulationMIC(X,Y).getMIC()