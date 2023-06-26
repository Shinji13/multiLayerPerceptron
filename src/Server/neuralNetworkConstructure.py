import numpy as np
from NeuralGraph import *
from queue import Queue


class neural_Network:
     def __init__(self,networkStructure,mode,activationFunction):
          # mode is either multilabel-classification , unique-classification or regression ## activation is either softplus or Relu
          self.activationFunction=activationFunction
          self.mode=mode
          self.networkStructure=[]
          for i in range(1,len(networkStructure)):
               currentWeights=np.random.randn(networkStructure[i],networkStructure[i-1]+1)
               self.networkStructure.append(currentWeights) 
     def getNetworkTrainingSize(self) :
           return (self.networkStructure[0].shape[1] - 1 , self.networkStructure[-1].shape[0])            

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
           elif self.mode==2:
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
           
     def feedForward(self,input,label):
            feed_graph=Neural_Graph()
            currentInputArray=Net_Inputs(0,input)               
            for i in range(0,len(self.networkStructure)-1):
                raw_output=self.raw_Calculation(feed_graph,currentInputArray,i)                                                           
                currentInputArray=self.activation_Calculation(feed_graph,raw_output,i)
            network_output=self.output_calculation(currentInputArray,feed_graph)
            loss=self.loss_calculation(feed_graph,network_output,label)
            return (loss,feed_graph)

     def backpropagation(self,network_graph,root):
           explored=set()
           queue=Queue()
           queue.put(root)
           while not queue.empty():
                 current=queue.get()
                 if current not in explored:
                       explored.add(current)    
                       neighbors=network_graph.nodesMap[current]
                       for neighbor in neighbors:
                             current.backward_Pass(neighbors,neighbor)     
                             if neighbor !="inp" and neighbor!="par":
                                   queue.put(neighbors[neighbor])            

     def one_batch_update(self,learning_rate,inputSet,labels):
            list_of_graphs=[]   
            loss_average=0   
            for i in range(0,len(inputSet)):
                  root,graph=self.feedForward(inputSet[i],labels[i])
                  self.backpropagation(graph,root)
                  list_of_graphs.append(graph)
                  loss_average+=root.value
            self.update_Parameters(list_of_graphs,learning_rate)
            return  loss_average/len(inputSet)      
     
     def stochastic_gradient_descent(self,inputSet,labels,learning_rate):           
            for i in range(0,len(inputSet)):
                  currentInput=inputSet[i]
                  currentLabel=labels[i]
                  root,graph=self.feedForward(currentInput,currentLabel)
                  self.backpropagation(graph,root)       
                  self.update_Parameters(graph,learning_rate)

     def update_Parameters(self,list_feed_graph,learning_rate):
                  batch_size=len(list_feed_graph)
                  for i in range(0,len(self.networkStructure)):
                        step=0
                        for j in range(0,batch_size):
                              step+=list_feed_graph[j].get_parameters_gradient(i)
                        self.networkStructure[i]= self.networkStructure[i]-learning_rate*(step/batch_size)   
      
     def batch_gradient_descent(self,learning_rate,batchSet,labels,loss_threshold,max_iterations):
             previous_loss=self.one_batch_update(learning_rate,batchSet,labels)
             converage=False
             iteration=0
             while not converage:                    
                   current_loss=self.one_batch_update(learning_rate,batchSet,labels)
                   if abs(current_loss-previous_loss)  < loss_threshold or iteration==max_iterations:
                         converage=True              
                   iteration+=1
                   previous_loss=current_loss
     
     def test(self,inputs):
           test_results=[]
           for row in inputs:
              feed_graph=Neural_Graph()
              currentInputArray=Net_Inputs(0,row)               
              for i in range(0,len(self.networkStructure)-1):
                raw_output=self.raw_Calculation(feed_graph,currentInputArray,i)                                                           
                currentInputArray=self.activation_Calculation(feed_graph,raw_output,i)
              network_output=self.output_calculation(currentInputArray,feed_graph)
              test_results.append((row,network_output.value))
           return test_results
     



                                                                                                    