import numpy as np
import math 
import random as random

class MLP_Constructor:
      def __init__(self,numberOfFeatures,LayersStructure,learningRate):
            self.numberOfFeatures=numberOfFeatures
            self.learningRate=learningRate
            self.network_weights=[]
            numberOfWeightsPerLayer=numberOfFeatures+1
            for i in range(0,len(LayersStructure)):
                  currentLayer=np.random.rand(LayersStructure[i],numberOfWeightsPerLayer)
                  self.network_weights.append(currentLayer)
                  numberOfWeightsPerLayer=LayersStructure[i]+1

      def sigmoid(self,x):
            return 1/(1+math.exp(-x)) 
      
      def dsigmoid(self,x) :
            return x*(1-x)    
      
      def feedForward(self,inputArray):
            #inputArray is numpy array             
            outputsArray=[]
            currentInputArray=np.insert(inputArray,0,1)    
            currentInputMatrix=np.asmatrix(currentInputArray).transpose()        
            for i in range(0,len(self.network_weights)):
                resualtBeforeActiviation=np.dot(self.network_weights[i],currentInputMatrix)
                matrixSigmoid=np.vectorize(self.sigmoid)                
                resualtAfterActiviation=matrixSigmoid(resualtBeforeActiviation)
                outputsArray.append(resualtAfterActiviation.copy())
                currentInputMatrix=np.insert(resualtAfterActiviation,0,1,axis=0)
            return outputsArray
      
      def isValidNetworkOutput(self,networkOutput,labeledOUtput,threshold):
              isValid=True
              for i in range(0,networkOutput.shape[0]):
                    if abs(networkOutput[i,0] -labeledOUtput[i,0])> threshold:
                          isValid=False
                          break
              return isValid
      
      
      def outLayerGradient(self,expectedOutput,networkOutput):
            matrixExpectedOutput=np.asmatrix(expectedOutput).transpose()            
            dsigmoidMatrix=np.vectorize(self.dsigmoid)
            derivative=dsigmoidMatrix(networkOutput)
            error=(matrixExpectedOutput-networkOutput)
            return (error,np.multiply(error,derivative))
      
      def hiddenLayerGradient(self,prevouisLayerError,currentLayerOutput,LayerIndex):
            dsigmoidMatrix=np.vectorize(self.dsigmoid)
            derivative=dsigmoidMatrix(currentLayerOutput)
            targetedWeights=self.network_weights[LayerIndex+1][:,1:].transpose()          
            error=np.dot(targetedWeights,prevouisLayerError)
            return (error,np.multiply(derivative,error))

      def backpropagatation(self,networkOutput,expectedOutput,input): 
        (error,gradient)=self.outLayerGradient(expectedOutput,networkOutput=networkOutput[-1])
        currentInput=None
        for i in range(len(self.network_weights)-1,0-1,-1):
            if(i==0):
                  currentInput=np.insert(input,0,1,1)
            else :
                  currentInput=np.insert(networkOutput[i-1].transpose(),0,1,1)
            currentGradient=gradient
            (error,gradient)=self.hiddenLayerGradient(error,networkOutput[i-1],i-1)
            delta=np.dot(self.learningRate*currentGradient,currentInput)
            self.network_weights[i]=self.network_weights[i]+delta
            print(self.network_weights[i])
            print("\n")
            
      def training(self,trainingData,numberOfInterations,threshold):
            #threshold is basically number from 0 to 1 that tell us if output is relatively good with respect to labeled output and decide whetehr to  backpropagate or not
            missClassification=0
            while numberOfInterations>0:
                  randomRaw=math.floor((random.random()*trainingData.shape[0]))
                  row=trainingData[randomRaw]
                  inputArray=row[0:-self.network_weights[-1].shape[0]]
                  expectedOutput=row[-self.network_weights[-1].shape[0]:]
                  networkOutput=self.feedForward(inputArray)
                  isValid=self.isValidNetworkOutput(networkOutput[-1],np.asmatrix(expectedOutput).transpose(),threshold)
                  if not isValid:
                        self.backpropagatation(networkOutput=networkOutput,expectedOutput=expectedOutput,input=np.asmatrix(inputArray))
                        missClassification+=1
                  numberOfInterations-=1                                        
            return missClassification    
     
mv2=MLP_Constructor(2,[2,1],0.1)            



