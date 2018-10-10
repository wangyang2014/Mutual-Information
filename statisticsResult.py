# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 21:38:38 2018

@author: wangyang
"""
import numpy as np
import random 
from CalculationMI import CalculationMI
from Func_matualInfo import Func_matualInfo
from MIC import calulationMIC

class statisticsResult():
    def __init__(self,m,n,diminsion,datapath,labelpath,readfunc):
        self.n = n
        self.m = m
        self.diminsion = diminsion
        self.datapath = datapath
        self.labelpath = labelpath
        self.readfunc = readfunc #this is interface about read data or label file function 
        self.methon = None
      
    def __SNPbootstrap(n,m,diminsion):
        resample = np.zeros([n,m],type='int32')
        for i in range(0,n):
            for j in range(0,m):
                resample[i][j] = random.randint(0,diminsion)
        return resample
    
    def __getdata(self):
        self.data = self.readfunc(self.datapath)
        self.label = self.readfunc(self.labelpath)
        
    def __choseMethon(self,methon_chose):
        if(1 == methon_chose):
            self.methon = Func_matualInfo
        elif(2 == methon_chose):
            self.methon = CalculationMI
        else:
            self.methon = calulationMIC
    def __MICsort(self,sample,index,compare):
        class sortvalue():
            def __init__(self,MI,index):
                self.MI = MI
                self.index = index
        def __repr__(self):
            return repr((self.MI,self.index))
                
        size = sample.shape
        MICdata = []
        MIsort = []
        sortindex = []
        if(compare == -1):
            for i in range(0,size[1]):
                MI = self.methon(sample[:,i],self.label[index])
                MICdata.append(MI)
                MIsort.append([MI,i])
        else:
            for i in range(0,size[1]):
                MI = self.methon(sample[:,i],sample[:,index])
                MICdata.append(MI)
                MIsort.append(sortvalue(MI,i))
        sortdata = sorted(MIsort,key = lambda sortvalue: sortvalue.MI)
        for data in sortdata:
            sortindex.append(data.index)
        return MICdata,sortindex
            
    def statisticsResult(self,methon_chose,compare):
        resample = self.__SNPbootstrap(self.n,self.m = m,self.diminsion)
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