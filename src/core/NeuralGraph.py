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
class Neuron:
    def __init__(self,layer,type):
        self.layer=layer
        self.type=type
        self.value=0
        self.gradient=1
    def __hash__(self):
        return hash(self.type) ^ hash(self.layer)   
    
class Net_Inputs(Neuron):
    def __init__(self,layer,inputArray):
        super().__init__(layer,"000")        
        self.value=np.asmatrix(inputArray).transpose()   

class Layer_Parameters(Neuron):# weights and biases for layer i to layer i+1 as matrix
    def __init__(self,layer,parameterReference):
        super().__init__(layer,"001")    
        self.value=parameterReference    

class Raw_Layer_Outputs(Neuron): # output of layer before applying the activation function
    def __init__(self,layer):
        super().__init__(layer,"010")  

    def forward_Pass(self,layer_inputs,layer_weights):  
        input_with_bias=np.insert(layer_inputs.value,0,1,axis=0)
        self.value=np.dot(layer_weights.value,input_with_bias)   

    def Backward_Pass(self,children_Map,derivationVariable):
        layer_inputs=children_Map["000"] if children_Map["000"] != None else children_Map["011"]
        input_with_bias=np.insert(layer_inputs.value,0,1,axis=0)
        layer_params=children_Map["001"]
        if derivationVariable=="001":
            layer_params.gradient=np.dot(self.gradient,input_with_bias.transpose())
        else :
            layer_inputs.gradient=np.dot(layer_params.value[:,1:].transpose(),self.gradient)             

class ReLu_Matrix(Neuron):
    def __init__(self, layer):        
        super().__init__(layer, "011")
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
        super().__init__(layer, "100")
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
        super().__init__(layer, "101")
    def forward_Pass(self,raw_Layer_Output):
        math=Neural_Network_Math()
        self.value=math.SoftMax(raw_Layer_Output.value)
    def backward_Pass(self,children_Map,derivationVariable):
        math=Neural_Network_Math()
        raw_Layer_Outputs=children_Map[derivationVariable]
        localGradient=np.zeros(self.value.shape)
        for i in range(0,self.value.shape[0]):
            localGradient[i][0]=math.dSoftMax(self.value,i)
        raw_Layer_Outputs.gradient=np.multiply(self.gradient,localGradient)
            
