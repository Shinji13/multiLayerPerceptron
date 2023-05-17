import numpy as np
import math 

class MLP_Constructor:
      def __init__(self,numberOfFeatures,LayersStructure,learningRate):
            self.numberOfFeatures=numberOfFeatures
            self.learningRate=learningRate
            self.network_weights=[]
            numberOfWeightsPerLayer=numberOfFeatures+1
            for i in range(0,len(LayersStructure)):
                  currentLayer=np.ones(shape=(LayersStructure[i],numberOfWeightsPerLayer))
                  self.network_weights.append(currentLayer)
                  numberOfWeightsPerLayer=LayersStructure[i]+1
      def sigmoid(self,x):
            return 1/(1-math.exp(-x))      
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
mv2=MLP_Constructor(2,[2,3,2],0.1)            

resualts=mv2.feedForward([0,1])