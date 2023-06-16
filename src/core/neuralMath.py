import math
import numpy as np

class Neural_Network_Math:
     def Sigmoid(self,x): 
            return 1/(1+math.exp(-x))       
     def dSigmoid(self,x) :
            return x*(1.0-x)     
     def ReLu(self,x):
           return max(0,x)
     def dReLu(self,x):
           return 0 if x <0 else 1
     def SoftMax(self,output_Vals):
           denominator=0
           softmax_Output=np.zeros(output_Vals.shape)
           for i in range(0,output_Vals.shape[0]):
                  denominator+=math.exp(output_Vals[i][0])
           for i in range(0,output_Vals.shape[0]):                 
               numerator=math.exp(output_Vals[i][0])  
               softmax_Output[i][0]=numerator/denominator
           return softmax_Output
     def dSoftMax(self,softMaxOutput,derivativeVariable):
           derivativeSum=0
           for i in range(0,softMaxOutput.shape[0]):
                  if i==derivativeVariable :
                    derivativeSum+=softMaxOutput[derivativeVariable][0]*(1-softMaxOutput[derivativeVariable][0])
                  else :
                    derivativeSum+=-softMaxOutput[derivativeVariable][0]*softMaxOutput[i][0]
           return derivativeSum
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
