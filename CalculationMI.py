# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 15:56:55 2018

@author: wangyang
"""

import numpy as np
import matplotlib.pyplot as plt
import math

class CalculationMI():
    def __init__(self,X,Y):
        self.X = X
        self.Y = Y
        
    def __getUnique(self,X):
        dictuniqueX = {}
        XList = []
        
        for i in self.X:
            dictuniqueX[str(i)] = i
        
        for key in dictuniqueX:
            XList.append(dictuniqueX[key])
            
        return XList
    
    def __findAllIndex(self,listset,value):
        length = len(listset)
        AllIndex = []
        position = -1
        
        while(True):
            try:
                position = listset.index(value,position+1,length)
                AllIndex.append(position)
            except:
                return AllIndex
    
    def __intersect(self,indexX,indexY):
        tmp = [val for val in indexX if val in indexY]
        return tmp
    
    def __getMI(self,probabilityXY):
        eps = math.pow(10,-10)
        distrbutionX = np.sum(probabilityXY,axis=1)
        HX = np.multiply(distrbutionX , np.log2(1/(np.mat(distrbutionX)+eps)))
        
        distrbutionY = np.sum(probabilityXY,axis=0)
        HY = np.multiply(distrbutionY , np.log2(1/(np.mat(distrbutionY)+eps)))
        
        HXY = np.multiply(probabilityXY,np.log2(1./(probabilityXY+eps)))
        MI = np.sum(HX) + np.sum(HY) - np.sum(np.sum(HXY))
        
        return MI
        
    def __Calculation(self):
        total = len(self.X)
        XList = self.__getUnique(self.X)
        YList = self.__getUnique(self.Y)
            
        n = len(XList)
        m = len(YList)
        
        probabilityXY = np.zeros([n,m])
        
        for i in range(0,n):
            indexX = self.__findAllIndex(XList,i)
            for j in range(0,m):
                indexY = self.__findAllIndex(YList,j)
                probabilityXY[i,j] = len(self.__intersect(indexX,indexY))/total
                
        return self.__getMI(probabilityXY)
    
    def runapp(self):
        return self.__Calculation()
def readdata(filepath,splitchar = ''):
    data = []
    with  open(filepath,'r') as ftp:
        for line in ftp.readlines():
            data = data + line.split(splitchar)
    return data

if __name__ == '__main__': 
    X = [1,2,3,4]
    Y = [1,2,3,5]
    MI = CalculationMI(X,Y).runapp()
   