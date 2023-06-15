import numpy as np
import math

class Neural_Network_Math:
     def Sigmoid(self,x): 
            return 1/(1+math.exp(-x))       
     def dSigmoid(self,x) :
            return x*(1.0-x)     
     def ReLu(self,x):
           return max(0,x)
     def dReLu(self,x):
           return 0 if x <=0 else 1
     def SoftMax(self,output_Vals):
           denominator=0
           for i in range(0,output_Vals.shape[0]):
                  denominator+=math.exp(output_Vals[i][0])
           for i in range(0,output_Vals.shape[0]):                 
               numerator=math.exp(output_Vals[i][0])  
               output_Vals[i][0]=numerator/denominator
           return output_Vals.transpose()
     def dSoftMax(self,softMaxOutput,i,j):
           if i==j :
                 return softMaxOutput[i]*(1-softMaxOutput[i])
           else :
                 return -softMaxOutput[i]*softMaxOutput[j]
     def CrossEntropy(self,softMaxOutput,label):
           if len(np.shape(label))==0:
                 return -math.log(softMaxOutput[label],math.e)
           else :
                 crossEntropyResualt=0
                 for i in range(0,len(label)):
                       crossEntropyResualt+=-math.log(softMaxOutput[i],math.e)*label[i]
                 return crossEntropyResualt
     def Loss_CrossEntropy(self,BatchOutputs,labels):
           Total_Loss=0
           for i in range(0,len(BatchOutputs)):
                 Total_Loss+=self.CrossEntropy(BatchOutputs[i],labels[i])
           return Total_Loss/len(labels)
     def Loss_SSR(self,BatchOutputs,labels):
           sum=0
           for i in range(0,len(labels)):
                 resudal=labels[i]-BatchOutputs[i][0]
                 sum+=pow(resudal,2)
           return sum/len(labels)   


class neural_Network:
     def __init__(self,networkStructure,mode):
          # mode is either multilabel-classification , unique-classification or regression ## activation is either sigmoid or Relu
          self.math=Neural_Network_Math()
          self.activationFunction=np.vectorize(self.math.ReLu) 
          self.mode=mode
          self.networkStructure=[]
          for i in range(1,len(networkStructure)):
               currentWeights=np.random.randn(networkStructure[i],networkStructure[i-1]+1)
               self.networkStructure.append(currentWeights) 
     def CalculateOutputs(self,previousLayerOutputs):
            outputsBeforeActiviation=np.dot(self.networkStructure[-1],previousLayerOutputs)             
            if self.mode==0:
                  return outputsBeforeActiviation
            elif self.mode==1:
                matrixSigmoid=np.vectorize(self.math.Sigmoid)
                resualtAfterActiviation=matrixSigmoid(outputsBeforeActiviation)
                return resualtAfterActiviation
            else :
                  return self.math.SoftMax(outputsBeforeActiviation)                   
     def feedForward(self,input):
            outputsArray=[]
            currentInputArray=np.insert(input,0,1)    
            currentInputMatrix=np.asmatrix(currentInputArray).transpose()        
            for i in range(0,len(self.networkStructure)-1):
                resualtBeforeActiviation=np.dot(self.networkStructure[i],currentInputMatrix)                     
                resualtAfterActiviation=self.activationFunction(resualtBeforeActiviation)
                outputsArray.append(np.asarray(resualtAfterActiviation).ravel())
                currentInputMatrix=np.insert(resualtAfterActiviation,0,1,axis=0) 
            lastLayerOutput=self.CalculateOutputs(currentInputMatrix)                           
            outputsArray.append(np.asarray(lastLayerOutput).ravel())
            return outputsArray      
     def extractOutputs(self,cache):
           batchOutputs=[]    
           for sampleOutPut in cache:
                 batchOutputs.append(sampleOutPut[-1])
           return batchOutputs
     def calculateCost(self,batchOutputs,labels):
           if self.mode==0:
              return self.math.Loss_SSR(batchOutputs,labels)
           else :
              return self.math.Loss_CrossEntropy(batchOutputs,labels)
     def train(self,learningRate,costThreshold,trainingBatch,labels,iterations):
           lastCost=-1
           for i in range(0,iterations):
                 cache=[]
                 for sample in trainingBatch:
                        sampleOutPuts=self.feedForward(sample)
                        cache.append(sampleOutPuts)
                 batchOutPuts=self.extractOutputs(cache)  
                 currentCost=self.calculateCost(batchOutPuts,labels)                       
                 lastCost=currentCost
                 print("Iteration number %d with cost = %f" % (i,lastCost))
                 #backpropagate
           return True
         


net=neural_Network([2,2,2],2)

net.train(0.1,0.001,[[1,2],[2,4],[4,5]],[0,0,0],10)