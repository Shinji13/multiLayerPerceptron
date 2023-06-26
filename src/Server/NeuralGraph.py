from neuralMath import Neural_Network_Math
import numpy as np


class Neural_Graph:
    def __init__(self):
        self.nodesMap={}
    def addNode(self,parent,childrenList):
        if self.nodesMap.get(parent) == None:
            self.nodesMap[parent]={}
            for child in childrenList:
                self.nodesMap[parent][child.type]=child
                if self.nodesMap.get(child) == None:
                    self.nodesMap[child]={}         
    def get_parameters_gradient(self,layer):
        for node in self.nodesMap:
            if node.type=="par" and node.layer==layer: 
                 return node.gradient     
    def get_node(self,layer,type):
        for node in self.nodesMap:
            if node.layer==layer and node.type==type:              
                   return node.value
    def showCase(self):
        for node in self.nodesMap:
            print("layer :" ,node.layer , "type :",node.type , " value :", node.value , " gradient :" ,node.gradient,"\n")                    
class Neuron:
    def __init__(self,layer,type):
        self.layer=layer
        self.type=type
        self.value=0
        self.gradient=1
    def __hash__(self):
        return hash(self.type) ^ hash(self.layer)   
    def getValuesAsArray(self):
        return np.ravel(self.value)
    
class Net_Inputs(Neuron):
    def __init__(self,layer,inputArray):
        super().__init__(layer,"inp")        
        self.value=np.asmatrix(inputArray).transpose()   

class Layer_Parameters(Neuron):# weights and biases for layer i to layer i+1 as matrix
    def __init__(self,layer,parameterReference):
        super().__init__(layer,"par")    
        self.value=parameterReference    

class Raw_Layer_Outputs(Neuron): # output of layer before applying the activation function
    def __init__(self,layer):
        super().__init__(layer,"raw")  

    def forward_Pass(self,layer_inputs,layer_weights):  
        input_with_bias=np.insert(layer_inputs.value,0,1,axis=0)
        self.value=np.dot(layer_weights.value,input_with_bias)   

    def backward_Pass(self,children_Map,derivationVariable):
        layer_inputs=children_Map["inp"] if "inp" in children_Map else children_Map["rel"] if "rel" in children_Map else children_Map["sop"]
        layer_params=children_Map["par"]
        if derivationVariable=="par":
            input_with_bias=np.insert(layer_inputs.value,0,1,axis=0)
            layer_params.gradient=np.dot(self.gradient,input_with_bias.transpose())
        else:
            layer_inputs.gradient=np.dot(layer_params.value[:,1:].transpose(),self.gradient)             

class ReLu_Matrix(Neuron):
    def __init__(self, layer):        
        super().__init__(layer, "rel")
        math=Neural_Network_Math()
        self.relu_Matrix=np.vectorize(math.ReLu) 
        self.drelu_Matrix=np.vectorize(math.dReLu)

    def forward_Pass(self,raw_Layer_Output):
        self.value=self.relu_Matrix(raw_Layer_Output.value)

    def backward_Pass(self,children_Map,derivationVariable):
        raw_Layer_Outputs=children_Map[derivationVariable]
        raw_Layer_Outputs.gradient=np.multiply(self.gradient,self.drelu_Matrix(raw_Layer_Outputs.value))

class Sigmoid_Matrix(Neuron):
    def __init__(self, layer):        
        super().__init__(layer, "sig")
        math=Neural_Network_Math()
        self.sigmoidMatrix=np.vectorize(math.Sigmoid) 
        self.dsigmoidMatrix=np.vectorize(math.dSigmoid)

    def forward_Pass(self,raw_Layer_Output):
        self.value=self.sigmoidMatrix(raw_Layer_Output.value)

    def backward_Pass(self,children_Map,derivationVariable):
        raw_Layer_Outputs=children_Map[derivationVariable]
        raw_Layer_Outputs.gradient=np.multiply(self.gradient,self.dsigmoidMatrix(self.value))


class Softmax_matrix(Neuron):
    def __init__(self, layer):
        super().__init__(layer, "som")
    def forward_Pass(self,raw_Layer_Output):
        math=Neural_Network_Math()
        self.value=math.SoftMax(raw_Layer_Output.value)
    def backward_Pass(self,children_Map,derivationVariable):
        math=Neural_Network_Math()
        raw_Layer_Outputs=children_Map[derivationVariable]
        localGradient=[]
        for i in range(0,self.value.shape[0]):
             currentPartialDerivative=math.dSoftMax(self.value,i)
             localGradient.append(currentPartialDerivative)
        localGradient_Matrix=np.asmatrix(localGradient)
        raw_Layer_Outputs.gradient=np.dot(localGradient_Matrix,self.gradient)

class SoftPlus(Neuron):
    def __init__(self, layer):
        super().__init__(layer, "sop")
        math=Neural_Network_Math()
        self.softPlusMatrix=np.vectorize(math.SoftPlus) 
        self.dsoftPlusMatrix=np.vectorize(math.dSoftPlus)
    def forward_Pass(self,raw_Layer_Output):
        self.value=self.softPlusMatrix(raw_Layer_Output.value)

    def backward_Pass(self,children_Map,derivationVariable):
        raw_Layer_Outputs=children_Map[derivationVariable]
        raw_Layer_Outputs.gradient=np.multiply(self.gradient,self.dsoftPlusMatrix(raw_Layer_Outputs.value))

class Sum_Squared_Residuals(Neuron):
     def __init__(self, layer):
        super().__init__(layer, "ssr")

     def forward_Pass(self,labels,last_layer_output):
        math=Neural_Network_Math()
        self.value=math.Loss_SSR(last_layer_output.value,labels.value)
     def backward_Pass(self,children_Map,derivationVariable):
         labels=children_Map["inp"]
         network_outputs=children_Map["raw"]
         if derivationVariable =="inp":
             local_gradient=2*(labels.value-network_outputs.value)
             labels.gradient=np.multiply(self.gradient,local_gradient)
         else :
             local_gradient=2*(network_outputs.value-labels.value)
             network_outputs.gradient=np.multiply(self.gradient,local_gradient)

class Cross_Entropy(Neuron):
      def __init__(self, layer):
        super().__init__(layer, "cre")

      def forward_Pass(self,labels,last_layer_output):
        math=Neural_Network_Math()
        self.value=math.Loss_CrossEntropy(last_layer_output.value,labels.value)              
      
      def backward_Pass(self,children_Map,derivationVariable):
           labels=children_Map["inp"]
           network_outputs=children_Map["som"] if "som" in children_Map else children_Map["sig"]
           if derivationVariable =="inp":
             local_gradient=-np.log(network_outputs.value)
             labels.gradient=np.multiply(self.gradient,local_gradient)
           else :
             log_derivative=network_outputs.value/np.power(network_outputs.value,2)
             local_gradient=np.multiply(-log_derivative,labels.value)
             network_outputs.gradient=np.multiply(self.gradient,local_gradient)


