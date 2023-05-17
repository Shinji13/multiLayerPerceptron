import numpy as np


class multiLayer_Perceptron:
    def __init__(self,numberOfFeatures,numberOfHiddenNeurons,numberOfOutputs,learningRate):
        self.numberOfFeatures=numberOfFeatures
        self.numberOfHiddenNeurons=numberOfHiddenNeurons
        self.numberOutputs=numberOfOutputs
        self.learningRate=learningRate
        self.hiddenLayer=np.zeros(shape=(numberOfHiddenNeurons,numberOfFeatures+1))
        self.outPutLayer=np.zeros(shape=(numberOfOutputs,numberOfHiddenNeurons+1))
    def print(self):
        print("hidden layer weights :",self.hiddenLayer)
        print("output layer weights :",self.outPutLayer)
    
    def checkValidSet(self,layer,trainingSet):        
        validShape=self.hiddenLayer.shape[1] if layer==0 else self.outPutLayer.shape[1]
        if(trainingSet.shape[1]!=validShape):
            raise Exception("Training set is not valid set")                   

    def retrieveNeuronWeights(self,layer,neuronIndex):
        if layer ==0:
            return self.hiddenLayer[neuronIndex]
        else :
            return self.outPutLayer[neuronIndex]

    def UniqueNeuronLearning(self,layer,neuronIndex,trainingSet,numIterations):
        self.checkValidSet(layer=layer,trainingSet=trainingSet)        
        labels=trainingSet[:,-1]
        features=trainingSet[:,:-1]    
        errorsList=[]
        w=self.retrieveNeuronWeights(layer=layer,neuronIndex=neuronIndex)
        for iter in range(0,numIterations):
          errors=0          
          for feautre,label in zip(features,labels):
             x=np.insert(feautre,0,1)
             y=x*w
             target=1 if np.sum(y)>0  else 0
             delta=label-target
             if delta!=0:
                 errors+=1
                 w+=x*delta*self.learningRate
          errorsList.append(errors)
        return (errorsList,w)    
    
    def globalLearning(self,trainingSet,numIterations):
        inputSet=trainingSet[:,0:self.numberOfFeatures]
        hiddenSet=trainingSet[:,self.numberOfFeatures:self.numberOfFeatures+self.numberOfHiddenNeurons]
        outPutSet=trainingSet[:,self.numberOfFeatures+self.numberOfHiddenNeurons:]  
        # relaxing hidden layer 
        rs1=self.hiddenLayerLearning(inputSet,hiddenSet,numIterations)
        # relaxing output layer 
        rs2=self.outputLayerLearning(hiddenSet,outPutSet,numIterations)
        return (rs1,rs2)
    
    def hiddenLayerLearning(self,inputSet,hiddenSet,numIterations):
        hiddenSetResualts=[]     
        for i in range(0,self.numberOfHiddenNeurons) :
            wantedNeuronSet=np.copy(hiddenSet[:,i])            
            wantedNeuronSet.shape=(wantedNeuronSet.shape[0],1)
            targetSet=np.concatenate((inputSet,wantedNeuronSet),axis=1)
            resualt= self.UniqueNeuronLearning(0,i,targetSet,numIterations=numIterations)
            hiddenSetResualts.append(resualt)
        return hiddenSetResualts

    def outputLayerLearning(self,hiddenSet,outPutSet,numIterations):
        outPutSetResualts=[]            
        for i in range(0,self.numberOutputs) :
            wantedNeuronSet=np.copy(outPutSet[:,i])
            wantedNeuronSet.shape=(wantedNeuronSet.shape[0],1)
            targetSet=np.concatenate((hiddenSet,wantedNeuronSet),axis=1)
            resualt= self.UniqueNeuronLearning(1,i,targetSet,numIterations=numIterations)
            outPutSetResualts.append(resualt)
        return outPutSetResualts    
    def testNetwork(self,feauture):
        if len(feauture)!=self.numberOfFeatures:
           raise Exception("your feauture is invalid")
        x=np.insert(feauture,0,1)        
        # hidden neurons resulat
        hiddenNeuronsResualts=np.zeros(shape=(self.numberOfHiddenNeurons,))
        for i in range(0,self.numberOfHiddenNeurons):
            y=x*self.hiddenLayer[i]
            target=1 if np.sum(y)>0  else 0
            hiddenNeuronsResualts[i]=target
        
        x=np.insert(hiddenNeuronsResualts,0,1)  
        finalOutput=[]
        for i in range(0,self.numberOutputs):
            y=x*self.outPutLayer[i]
            target=1 if np.sum(y)>0  else 0
            finalOutput.append(target)
        return finalOutput



nt=multiLayer_Perceptron(2,2,1,0.1)

xorTrainingSet=np.array([[0,1,0,1,1],[1,1,0,0,0],[1,0,1,0,1],[0,0,0,0,0],[0,1,0,1,1],[1,1,0,0,0],[0,0,0,0,0],[0,1,0,1,1],[1,1,0,0,0],[1,0,1,0,1],[0,0,0,0,0]])

tuple=nt.globalLearning(xorTrainingSet,20)
resualt=nt.testNetwork(np.array([0,0]))
print(resualt)