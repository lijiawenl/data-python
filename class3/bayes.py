# -*- coding: utf-8 -*-
"""
Created on Mon May 08 18:26:48 2017

@author: DELL
"""
from numpy import*
def loadDataSet():
    postingList = [['my','dog','has','flea','problems','help','please'],\
                   ['maybe','not','take','him','to','dog','park','stupid'],\
                   ['my','dalmation','is','so','cute','I','love','him'],\
                   ['stop','posting','stupid','worthless','garbage'],\
                   ['mr','licks','ate','my','steak','how','to','stop','him'],\
                   ['quit','buying','worthless','dog','food','stupid',]]
    classVec = [0,1,0,1,0,1]
    return postingList, classVec
##创建自己的字符集
def createVocabList(dataSet):
    vocabSet = set([])
    for documen in dataSet :
        vocabSet = vocabSet | set(documen) ##| 用于求两个集合的并集，可以理解为数学上的
    return list(vocabSet)

#返回一个基于词库的单条记录的词向量，词集的模型
def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0] *len(vocabList)#创建一个含有所有元素为0 的向量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary" % word
    return returnVec

#返回一个基于词库的单条记录的词向量，词集的模型
def bagOfWords2Vec(vocabList,inputSet):
    returnVec = [0] *len(vocabList)#创建一个含有所有元素为0 的向量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else: print "the word: %s is not in my Vocabulary" % word
    return returnVec


def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = zeros(numWords); p1Num = zeros(numWords)
    p0Denom = 0.0; p1Denom = 0.0;
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]#每个词条出现的话，matrix位置上对应为1,相加的和可用于计算p(w|c)
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num/p1Denom
    p0Vect = p0Num/p0Denom
    return p0Vect,p1Vect,pAbusive

##修改trainNB0中的缺陷
##1.修改初始化次数，防止出现p(w|0)或p(w|1)=0的情况
##初始化分母为2，因为1+1=2
##因为具体分类时，p(w|0)或p(w|1)连乘会很小，防止下溢，采用log值
def trainNB1(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)
    p0Denom = 2.0; p1Denom = 2.0;
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]#每个词条出现的话，matrix位置上对应为1,相加的和可用于计算p(w|c)
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)
    p0Vect = log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify*p1Vec) + log(pClass1) #log(p(w|0)*...*p(w|1)*p(c=1)),如果词项没有的话对应的vec2Classify
    p0 = sum(vec2Classify*p0Vec) + log(1.0-(pClass1))##的位置为零  这一步用到了numpy的矩阵的相乘
    if p1 >p0 :
        return 1
    else: return 0
    
##sample 1
def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) >2 ]

def spamTest():
    docList = []; classList =[]; fullText = [];
    for i in range(1,26):
        wordList = textParse(open('F:/Python/MLiA_SourceCode/machinelearninginaction/Ch04/email/spam/%d.txt' % i).read())
        docList.append(wordList)#open()统一打开为一个['','',]，readlines()按照行打开
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('F:/Python/MLiA_SourceCode/machinelearninginaction/Ch04/email/ham/%d.txt' % i).read())
        docList.append(wordList)#得到的结果放到空的list中去
        fullText.extend(wordList)
        classList.append(0)
    vocalbList = createVocabList(docList)
    trainingSet = range(50);testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])#删除一条从剩下的去选择
    trainMat = []; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocalbList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0Vect,p1Vect,pAbusive = trainNB1(array(trainMat),array(trainClasses))##array()得到的一定是matrix
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocalbList,docList[docIndex])
        if classifyNB(wordVector,p0Vect,p1Vect,pAbusive) != classList[docIndex]:
             errorCount += 1
    print 'the input error rate is: ',float(errorCount)/len(testSet)
        

#postingList, classVec =loadDataSet()

#myVocabList = createVocabList(postingList)

#returnVe =  setOfWords2Vec(myVocabList,postingList[1])

#trainMat = []

#for postinDoc in postingList:
 #   trainMat.append(setOfWords2Vec(myVocabList,postinDoc))

#p0Vect,p1Vect,pAbusive = trainNB1(trainMat,classVec)

spamTest()
