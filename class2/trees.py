# -*- coding: utf-8 -*-
"""
Created on Thu May 04 13:13:14 2017

@author: DELL
"""
from math import log
import operator
import treePlotter

def createDataSet():
    dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]#这是整数和字符串混合的数组
    labels=['no surfacing','flippers']
    return dataSet,labels##labels 是对应的特征的名字

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        currentLabel =featVec[-1]
        if currentLabel not in labelCounts.keys():##这个表述真有意思，好直白啊
            labelCounts[currentLabel] =0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    #print labelCounts
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        #print prob
        shannonEnt -= prob *log(prob,2)  #log base 2
    return shannonEnt

def splitDataSet(dataSet,axis,value):#axis=0 确保是第一个属性有一些疑惑
    retDataSet = []
    for featVec in dataSet:
        if  featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            #print featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])##剔除axis位置上的属性特征这里用了一个拼接
            #print featVec[axis+1:]
            retDataSet.append(reducedFeatVec)
    return  retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0;bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]#这种表达式我曹，得好好学习一下
        uniqueVals = set(featList) #set是集合的表示，类似于数学中的集合概念，列表，字典，字符串都可以作为参数
        newEntroy = 0.0
        for value in uniqueVals:
            subDataSet =  splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntroy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy-newEntroy
        if (infoGain >bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return  bestFeature##返回的是bestFeat的位置
        
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys() : classCount[vote] = 0
        classCount[vote]+= 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1),reverse=True)##对字典的键值进行排序,key返回的
    ##是一个函数，operator.itemgetter(1)定义函数，返回第二个位置的值。sorted返回的是一个List
    return sortedClassCount[0][0]##返回

def createTree(dataSet,labels):
    classList = [examples[-1] for examples in dataSet]
    if classList.count(classList[0]) == len(classList): ##count 函计算classList[0]这个值的个数
       return classList[0]
    if len(dataSet[0]) == 1:##表明只有一个属性的时候，返回该特征下类别数量最大的值是多少
       return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree ={bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]##确定bestFeat有几种取值label
    uniqueVals = set(featValues)
    for value in uniqueVals:##保证每一种value都可以的划分,for key value in Dict 是python 遍历字典的一种方式
       subLabels = labels[:]
       myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree
   
def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key :
            if type(secondDict[key]).__name__== 'dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else: classLabel = secondDict[key]
    return classLabel
            
            
def storeTree(inputTree,filename):
    import pickle 
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close
        
def grabTree(inputTree,filename):
    import pickle 
    fr = open(filename)
    return  pickle.load(fr)

   
dataSet,labels = createDataSet()

#shannonEnt = calcShannonEnt(dataSet)
#dataSet[0][-1]='maybe'
#shannonEnt = calcShannonEnt(dataSet)
#reDataSet = splitDataSet(dataSet,0,1)
#print reDataSet
#bestFeature = chooseBestFeatureToSplit(dataSet)
#myTree= createTree(dataSet,labels)##多重嵌套的字典来存储决策树
myTree = treePlotter.retriveTree(0)

lab = classify(myTree,labels,[1,0])
#print myTree