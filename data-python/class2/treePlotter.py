# -*- coding: utf-8 -*-
"""
Created on Thu May 04 22:09:10 2017

@author: DELL
"""

import matplotlib.pyplot as plt
decisionNode = dict(boxstyle = "sawtooth", fc="0.8")
leafNode = dict(boxstyle = "round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(NodeTxt, centerPt,parentPt,nodeType):
    createPlot.axl.annotate(NodeTxt,xy=parentPt,xycoords = 'axes fraction',\
                            xytext=centerPt,textcoords = 'axes fraction',
                            va = "center", bbox = nodeType, arrowprops = arrow_args)
def createPlot():
    fig = plt.figure(1, facecolor = 'white')
    fig.clf()#清空绘图
    createPlot.axl = plt.subplot(111, frameon=False)
    plotNode('a decision node', (0.3,0.5),(0.1,0.5),decisionNode)##第二参数是文本框的位置，第三个参数是箭头起点，根据定义的plotNode来解
    plotNode('a leaf node',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()
    
    
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:   numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':##魔术方法，
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else: thisDepth =1
        if thisDepth >maxDepth:maxDepth = thisDepth
    return maxDepth
        
def retriveTree(i):
    listOfTree = [{'no surfacing': {0:'no',1:{'flippers':\
                    {0:'no', 1:'yes'}}}},
                  {'no surfacing':{0:'no', 1: {'flippers'\
                    :{0:{'head':{0:'no',1:' yes'}}, 1:'no'}}}}]
    
    return listOfTree[i]

myTree=retriveTree(1)
numLeafs=getNumLeafs(myTree)
depthTree=getTreeDepth(myTree)
firstStr=myTree.keys()[0]
second=myTree[firstStr]
createPlot()
