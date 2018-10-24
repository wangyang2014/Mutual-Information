# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 20:47:18 2018

@author: Administrator
"""
import operator
class sortvalue():
    def __init__(self,MI,index):
        self.MIindex = MI
        self.index = index
def run():
    listdata = []
    for i in range(0,10):
        listdata.append(sortvalue(10-i,i))
    
    cmpfun = operator.attrgetter('MIindex')
    sorted(listdata,key = cmpfun)
    for i in range(0,10):
        print(listdata[i].MIindex,listdata[i].index)

run()