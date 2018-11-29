# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 12:33:14 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
import math
class IQMI():
    def __init__(self,data,label):
        self.data = data
        self.label = label
        
    def __getUnique(self,X):
        dictuniqueX = {}
        XList = []
        m,n = X.shape
        for i in range(0,m):
            for j in range(0,n):
                data = X[i,j]
                dictuniqueX[str(data)] = data
        
        for key in dictuniqueX:
            XList.append(dictuniqueX[key])
            
        return XList
    def __normal(self,x,mu,sigma):
        y_sig = np.exp(-(x - mu) ** 2 /(2* sigma **2))/(math.sqrt(2*math.pi)*sigma)
        return y_sig

    def Apprun(self):
        self.data = np.transpose(np.mat(self.data))
        data = self.data
        self.label = np.transpose(np.mat(self.label))
        label = self.label
        [m,n] = self.data.shape
        uniquelabel = self.__getUnique(self.label)
        Nc = len(uniquelabel)
        
        Xvalue = []
        count = []
        for i in range(0,Nc):
            position = self.label == uniquelabel[i]
            position = np.transpose(position)
            Xvalue.append(self.data[position][0])
            count.append(np.sum(position))
            
        pairdiff = np.zeros([m,m])
        for i in range(0,m):
            for j in range(0,m):
                value = self.data[i,:] - self.data[j,:]
                pairdiff[i,j] = np.sum(np.multiply(value,value))
                
        pairdiff = np.sqrt(pairdiff)
        vari = np.max(pairdiff)/2
        
        countarray = np.asarray(count)
        VALL = np.sum(self.__normal(np.ravel(pairdiff),0,vari)) * np.sum(np.multiply(countarray,countarray)) / (m**4)
        
        Vin = np.zeros([Nc])
        
        for i in range(0,Nc):
            b =  count[i]
            mincc = np.zeros([b,b])
            for j in range(0,b):
                for k in range(0,b):
                    value = Xvalue[i][:,j] - Xvalue[i][:,k]
                    mincc[j,k] = np.sum(np.multiply(value,value))
            
            Vin[i] = np.sum(self.__normal(np.ravel(mincc),0,vari))
            
        VIN = np.sum(Vin)/(m**2)
        
        Vbtw = np.zeros([Nc])
        for i in range(0,Nc):
            b =  count[i]
            mincc = np.zeros([m,b])
            for j in range(0,m):
                for k in range(0,b):
                    value = self.data[j,:] - Xvalue[i][:,k]
                    mincc[j,k] = np.sum(np.multiply(value,value))
            
            Vbtw[i] = np.sum(self.__normal(np.ravel(mincc),0,vari)) * b
            
        VBTW = np.sum(Vbtw)/(m**3)
        
        tmp = VIN + VALL - 2*VBTW
        
        if tmp<0:
            return 0
        else:
            return tmp
            
def getdata(datapath = 'datafeatures.csv',labelpath = 'label.csv'):
    dataset = pd.read_csv(datapath)
    feature = dataset.iloc[:,:].values
    labelset = pd.read_csv(labelpath)
    label = labelset.iloc[:].values
    return feature,label
    
if __name__ == '__main__': 
    feature,label = getdata()
    runapp = IQMI(data = feature[0:20,1],label = label[0:20])
    print(runapp.Apprun())
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            