# -*- coding: utf-8 -*-
"""
Created on Tue May 09 14:11:31 2017

@author: DELL
"""
from numpy import*

def loadDataSet():
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():##read():表示读取全部内容，readline()逐行读取
        lineArr = line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])#将b放在了参数里面
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

def sigmod(inx):
    return 1.0/(1+exp(-inx))
##全局的梯度下降
def gradAscent(dataMatIn,classLabels):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()##利用mat函数转化为numpy函数转置
    m,n = shape(dataMatrix)
    print m,n
    alpha = 0.001
    maxCycles = 500
    weights = ones((n,1))
    for k in range(maxCycles):
        h = sigmod(dataMatrix*weights)
        error = (labelMat-h)
        print 
        weights=weights+alpha*dataMatrix.transpose()*error##可以从多元向量函数来理解考虑
    return weights

#随机梯度下降法
def stocGradAscend0(dataMatrix,classLabels):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    for i in range(m):
        h = sigmod(sum(dataMatrix[i]*weights))
        error = classLabels[i]-h
        weights=weights + alpha * error * dataMatrix[i]
    return weights
#改进的随机梯度下降
def stocGradAscend1(dataMatrix,classLabels,numIters):
    m,n = shape(dataMatrix)
    weights = ones(n)
    for k in range(numIters):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+k+i)+0.01
            randomIndex =  int(random.uniform(0,len(dataIndex)))
            h = sigmod(sum(dataMatrix[randomIndex]*weights))
            error = classLabels[randomIndex]-h
            weights=weights + alpha * error * dataMatrix[randomIndex]
            del(dataIndex[randomIndex])
    return weights

def plotBestFit(weights):
    import matplotlib.pyplot as plt
    weights = array(weights)###将list转metrix才能weights[1]
    dataMat,labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])==1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    #画图的基本流程
    fig =plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c="red",marker ='s')
    ax.scatter(xcord2,ycord2,s=30,c="green")
    x= arange(-3.0,3.0,0.1)
    y = (-weights[0]-weights[1]*x)/weights[2] ##或者就(-weights[0][0]-weights[1][0]*x)/weights[2][0]
    ax.plot(x,y)
    plt.xlabel('x1');plt.ylabel('x2');
    plt.show()##感觉像是定义好所有模块，最后一个show拉开帷幕

dataMat,labelMat = loadDataSet()
#weights = gradAscent(dataMat,labelMat)
weights = stocGradAscend1(array(dataMat),labelMat,10)
#weights = array(weights)
#print weights[1][0]+1
plotBestFit(weights)
