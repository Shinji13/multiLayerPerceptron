import numpy as np
from neuralMath import Neural_Network_Math
from NeuralGraph import *

class neural_Network:
     def __init__(self,networkStructure,mode,activationFunction):
          # mode is either multilabel-classification , unique-classification or regression ## activation is either sigmoid or Relu
          self.activationFunction=activationFunction
          self.mode=mode
          self.networkStructure=[]
          for i in range(1,len(networkStructure)):
               currentWeights=np.random.randn(networkStructure[i],networkStructure[i-1]+1)
               self.networkStructure.append(currentWeights) 
     def raw_Calculation(self,graph,input,index):
          network_params=Layer_Parameters(index,self.networkStructure[index])
          raw_output=Raw_Layer_Outputs(index+1)
          raw_output.forward_Pass(input,network_params)  
          graph.addNode(raw_output,[input,network_params])    
          return raw_output
     
     def activation_Calculation(self,graph,raw,index):
          activation_Object=ReLu_Matrix(index+1) if self.activationFunction==0 else SoftPlus(index+1)
          activation_Object.forward_Pass(raw)
          graph.addNode(activation_Object,[raw])
          return activation_Object
     
     def output_calculation(self,previous_output,graph):           
           layer=len(self.networkStructure)-1
           raw=self.raw_Calculation(graph,previous_output,layer)
           if self.mode==0:
                 return raw
           elif self.mode==1:
                 sig=Sigmoid_Matrix(layer+1)
                 sig.forward_Pass(raw)
                 graph.addNode(sig,[raw])
                 return sig
           else:
                 softmax=Softmax_matrix(layer+1)
                 softmax.forward_Pass(raw)
                 graph.addNode(softmax,[raw])
                 return softmax
           
     def loss_calculation(self,graph,network_output,labels):
           layer=len(self.networkStructure)   
           labels_matrix=Net_Inputs(layer,labels)
           if self.mode==0:
                 ssr_loss=Sum_Squared_Residuals(layer)
                 ssr_loss.forward_Pass(labels_matrix,network_output)
                 graph.addNode(ssr_loss,[labels_matrix,network_output])
                 return ssr_loss
           else :
                 cross_loss=Cross_Entropy(layer)
                 cross_loss.forward_Pass(labels_matrix,network_output)
                 graph.addNode(cross_loss,[labels_matrix,network_output])
                 return cross_loss
           
     def feedForward(self,input,labels):
            feed_graph=Neural_Graph()
            currentInputArray=Net_Inputs(0,input)               
            for i in range(0,len(self.networkStructure)-1):
                raw_output=self.raw_Calculation(feed_graph,currentInputArray,i)                                                           
                currentInputArray=self.activation_Calculation(feed_graph,raw_output,i)
            network_output=self.output_calculation(currentInputArray,feed_graph)
            loss=self.loss_calculation(feed_graph,network_output,labels)
            return (loss,feed_graph)
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
         


net=neural_Network([2,2,1],2,0)


print(net.networkStructure)


