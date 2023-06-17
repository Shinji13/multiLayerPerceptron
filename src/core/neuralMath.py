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
     def SoftPlus(self,x):
           inside=1+math.exp(x)
           return math.log(inside,math.e)
     def dSoftPlus(self,x):
           exponent=math.exp(x)
           return exponent/(1+exponent)
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
           derivativeSum=[]
           for i in range(0,softMaxOutput.shape[0]):
                  if i==derivativeVariable :
                    derivativeSum.append(softMaxOutput[i][0]*(1-softMaxOutput[i][0]))
                  else :
                    derivativeSum.append(-softMaxOutput[derivativeVariable][0]*softMaxOutput[i][0])
           return derivativeSum
     def Loss_CrossEntropy(self,last_layer_output,labels):           
            log_Output=np.log(last_layer_output)
            error_matrix=np.multiply(-log_Output,labels)
            crossEntropyResualt=np.sum(error_matrix)
            return crossEntropyResualt     
     def Loss_SSR(self,last_layer_output,labels):
           diff=labels-last_layer_output
           diff_power=np.power(diff,2)
           ssr_Resualt=np.sum(diff_power)           
           return ssr_Resualt