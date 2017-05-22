# -*- coding: utf-8 -*-
"""
Created on Wed May 03 20:01:28 2017

@author: DELL
"""

import KNN
group,labels=KNN.createDataSet()
print group
print labels


def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1))-dataSet##tile(inx,(4,1))将inX以单元重复4ci,inx单元内重复1次http://www.cnblogs.com/yushuo1990/p/5879383.html
    sqDiffMat= diffMat**2
    sqDistance =sqDiffMat.sum(axis=1)
    distances =sqDistance**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1

    sortedClassCount =sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]##sorted函数对list操作，classCount是字典，因此可以迭代的是其可循环对象，是个list


print classify0([0,0],group,labels,3)


