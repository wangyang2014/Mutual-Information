# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:52:57 2018

@author: wangyang
"""
import csv 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

class Func_matualInfo():
    def __init__(self,datapath=None,labelpath=None,data=None,label=None):
        self.datapath = datapath
        self.labelpath = labelpath 
        self.data = data
        self.label = label
        
    def __readdata(self,filepath):
        mydata = []
        with open(filepath,'r')  as ftp:
            for line in csv.reader(ftp):
                mydata.append(line)
        return mydata
    
    def __getdata(self):
        if((self.datapath is None) and (self.labelpath is None)):
            pass
        else:
            self.data = np.asarray(self.__readdata(self.datapath),dtype = 'float')
            self.label = np.transpose(np.asarray(self.__readdata(self.labelpath),dtype = 'float'))
        
    
    def __dealwithData(self):
        self.data = self.data - np.min(self.data)
        self.label = self.label - np.min(self.label) + 1
    
    def __process(self):
        maxLabel = np.max(self.label)
        maxData = np.max(self.data) + 1
        row,column = np.shape(self.data)
        
        count = np.max(self.label) - np.min(self.label) + 1
        n, bins, patches = plt.hist(self.label,count)
        P_label = n/column
        Entropy_Label = np.sum(-P_label * np.log2(P_label + math.pow(10,-16)))
        
        if (row < 9):
            zz = []
            for i in range(0,row):
                zz.append(math.pow(maxData,i))
            zz = np.asarray(zz)
            
            hist_Label = np.zeros([maxData*row,maxLabel],dtype = 'float')
            tempIndex = np.dot(zz,self.data)
            
            for i in range(0,column):
                hist_Label[tempIndex[i],self.label[i]] += 1 
                
            sunHist = np.sum(hist_Label,1)
            repHist = np.transpose(np.asarray([sunHist,sunHist]))
            pHist_Label = hist_Label/(repHist+math.pow(10,-16))
            InfoIncre = - np.sum(np.log2(pHist_Label+math.pow(10,-16))*pHist_Label) * repHist
            
            MI = Entropy_Label - sum(InfoIncre)/column
            return MI
        else:
            mm = 0
            Hist_Label=np.zeros([row,column])
            Hist_Label[int(self.label[0]),mm] = 1
            Hist_SNP = np.zeros([row,column])
            Hist_SNP[:,mm] = self.data[:,0]
            
            #tempdata = np.zeros(row,column)
            
            for i in range(1,column):
                tempdata = np.copy(self.data[:,i])
                index = -1
                for k in range(0,mm+1):
                    if np.equal(Hist_SNP[:,k],tempdata).all():
                        index = k
                        break
                if index  == -1:
                    mm = mm + 1
                    Hist_SNP[:,mm] = np.copy(tempdata)
                    Hist_Label[int(self.label[i]),mm] = 1
                else:
                    Hist_Label[int(self.label[i]),index] = [int(self.label[i]),index] + 1
                    
            MI = mm
            InfoIncre=0
            for s in range(0,MI):
                tempsum = np.sum(Hist_Label[:,s])
                P = Hist_Label[:,s]/tempsum
                InfoIncre = InfoIncre - np.mat(np.log2(P + math.pow(10,-16)))*np.transpose(np.mat(P))*tempsum
            MI = Entropy_Label - InfoIncre/column
            return MI
        
    def run(self):
        self.__getdata()
        self.__dealwithData()
        return self.__process()
        
def getdata(datapath = 'datafeatures.csv',labelpath = 'label.csv'):
    dataset = pd.read_csv(datapath)
    feature = dataset.iloc[:,:].values
    labelset = pd.read_csv(labelpath)
    label = labelset.iloc[:].values
    return feature,label
    
if __name__ == '__main__': 
    feature,label = getdata()
    runapp = Func_matualInfo(data = feature,label = label)
    print(runapp.run())