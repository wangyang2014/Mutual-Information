# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 21:38:38 2018

@author: wangyang
"""
import pandas as pd
import numpy as np
import random 
from CalculationMI import CalculationMI
from func_mutualInfo import Func_matualInfo
import operator
#from MIC import calulationMIC

class statisticsResult():
    def __init__(self,m,n,diminsion,datapath,labelpath,readfunc):
        self.n = n
        self.m = m
        self.diminsion = diminsion
        self.datapath = datapath
        self.labelpath = labelpath
        self.readfunc = readfunc #this is interface about read data or label file function 
        self.methon = None
      
    def __SNPbootstrap(self,n,m,diminsion):
        resample = np.zeros([n,m],dtype='int32')
        for i in range(0,n):
            for j in range(0,m):
                resample[i][j] = random.randint(0,diminsion)
        return resample
    
    def __getdata(self):
        self.data = self.readfunc(self.datapath)
        self.label = self.readfunc(self.labelpath)
        
    def __choseMethon(self,methon_chose  = -1):
        if(1 == methon_chose):
            self.methon = Func_matualInfo
        elif(2 == methon_chose):
            self.methon = CalculationMI
       # else:
           # self.methon = calulationMIC
    def __MICsort(self,sample,index,compare):
        class sortvalue():
            def __init__(self,MI,index):
                self.MIindex = MI
                self.indexm = index
            #def __repr__(self):
                #return repr((self.MI,self.index))
        size = sample.shape
        MICdata = []
        MIsort = []
        sortindex = []
        if(compare == -1):
            for i in range(0,size[1]):
                #print(sample[:,i].shape,self.label[index,0].shape)
                MI = self.methon(sample[:,i],self.label[index,0]).runapp()
                MICdata.append(MI)
                MIsort.append(sortvalue(MI,i))
        else:
            for i in range(0,size[1]):
                #print(sample[:,i].shape,sample[:,compare].shape)
                MI = self.methon(sample[:,i],sample[:,compare]).runapp()
                MICdata.append(MI)
                MIsort.append(sortvalue(MI,i))
        #print(len(MIsort),type(MIsort[0]))
        cmpfun = operator.attrgetter('MIindex')
        sortdata = sorted(MIsort, key=cmpfun)
       # print('________________')
        for data in sortdata:
            sortindex.append(data.indexm)
        return MICdata,sortindex
            
    def Result(self,methon_chose,compare):
        resample = self.__SNPbootstrap(self.n,self.m,self.diminsion)
        result = []
        self.__getdata()
        self.__choseMethon(methon_chose)
        for i in range(0,self.n):
            index = resample[i,:]
            sample = self.data[index,:]
            MIC,indexMIC = self.__MICsort(sample,index,compare)
            labelMIC,labelindex = self.__MICsort(sample,index,-1)
            value = [MIC,indexMIC,labelMIC,labelindex]
            result.append(value)
        return result
    
def getdata(filepath):
    dataset = pd.read_csv(filepath)
    feature = dataset.iloc[:,:].values
    return feature

if __name__ == '__main__':
    apprun = statisticsResult(1000,1000,2000-1,'datafeatures.csv','label.csv',getdata)
    result = apprun.Result(2,98)
    print(type(result))