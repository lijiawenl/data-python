# -*- coding: utf-8 -*-
"""
Created on Wed May 03 19:36:33 2017

@author: DELL
"""
from numpy import *
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    ##array是什么样的数据结构
    labels = ['A','A','B','B']
    return group, labels



def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1))-dataSet##tile(inx,(4,1))将inX以单元重复4ci,inx单元内重复1次http://www.cnblogs.com/yushuo1990/p/5879383.html
    sqDiffMat= diffMat**2
    sqDistance =sqDiffMat.sum(axis=1)##sum函数
    distances =sqDistance**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1

    sortedClassCount =sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]##sorted函数对list操作，classCount是字典，因此可以迭代的是其可循环对象，是个list


def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return   
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(str(listFromLine[-1]))
        #classLabelVector.append(int(listFromLine[-1]))看输入的是str还是int类型，必须要进行强制的类型转换
        index += 1
    return returnMat,classLabelVector

datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
#print datingDataMat
#reset 可以清除之前的变量


def autoNorm(dataSet):
    minVal=dataSet.min(0)#选取当前列中的最小值，否则选择的是当前行的最小的值
    maxVal=dataSet.max(0)
    ranges= maxVal-minVal
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normData=dataSet-tile(minVal,(m,1))
    normData= normData/tile(ranges,(m,1))
    return normData,ranges,minVal

def datingClassTest():
    hoRatio =0.10
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat,ranges,minVal = autoNorm(datingDataMat)
    m= normMat.shape[0]
    numTestVecs = int (m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classfierResult = classify0(normMat[i,1],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is : %d" % (classfierResult, datingLabels[i])
        if (classfierResult != datingLabels[i]):
            errorCount += 1.0
    print " the total error is %f" %(errorCount/numTestVecs)
    print "the total test is %d"%(numTestVecs)
    
def classifyPerson():
    resultList=['not at all','in small doses','in  large doses']
    percentTats = float(raw_input(\
                "percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent filter miles earned per year"))
    iceCream = float(raw_input("liters of icream consumed earned per year"))
    datingDataMat,datingLabels = file2matrix('datingTestSet.txt')
    normMat,ranges,minVal = autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr-minVal)/ranges,normMat,datingLabels,3)
    print classifierResult 
    
#import matplotlib
#import matplotlib.pyplot as plt

#fig = plt.figure()
#ax = fig.add_subplot(111)#fig.add_subplot表示画几个图，类似matlab的subplot/float(numTestVecs)
#ax.scatter(datingDataMat[:,1],datingDataMat[:,2],10.0*array(datingLabels),15.0*array(datingLabels))##scatter表示散点图,(x,y)=
##(datingDataMat[:,1],datingDataMat[:,2])
#plt.plot
#normData=autoNorm(datingDataMat)
#print normData
#datingClassTest()

classifyPerson()