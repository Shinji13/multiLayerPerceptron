
from typing import Annotated
from fastapi import FastAPI,HTTPException,Form,UploadFile
from pydantic import BaseModel
import numpy as np
from  neuralNetworkConstructure import neural_Network
import csv
import codecs
import os

user_map={}
app=FastAPI()

class network_settings(BaseModel):
    mode:int
    activationFunction:int
    layers:list

def toNumpyArray(input_size, samples):
    string_arr = np.array(samples)
    float_list = string_arr.astype(float)
    batchData=float_list[:,0:input_size]
    labels=float_list[:,input_size:]
    return batchData,labels
       
def processFile(csv_file,requiredSize):
    file_iterator=codecs.iterdecode(csv_file,"utf-8")
    csv_iterator=csv.reader(file_iterator,delimiter=",")
    training_list=[]
    for row in csv_iterator:
        if requiredSize != len(row):
               raise  HTTPException(status_code=400,detail="The file doesnt match the network")
        training_list.append(row) 
    csv_file.close()
    return training_list   
    
def saveParams(user_hash,network):
    file_handler=open("../../static/res/"+user_hash+".csv","w+")
    csv_iterator=csv.writer(file_handler)
    params=network.networkStructure
    csv_iterator.writerow(["Weights are in form of wij in which i is the index of starting neuron from layer n and j is the index of ending neuron in layer n+1."])
    csv_iterator.writerow(["Biases are in form of bk where k represents the index of neuron this bias belongs to."])
    for i in range(0,len(params)) :
        csv_iterator.writerow(["L" +str(i)+" to L" +str(i+1)])    
        values=[]
        transpose_param=params[i].transpose()
        for k in range(0,transpose_param.shape[0]):
              for j in range(0,transpose_param.shape[1]):
                    param_type="w" +str(k-1)+str(j) if k>0 else "b"+str(j)
                    param_value=str(transpose_param[k,j])
                    values.append(param_type+":"+param_value)
        csv_iterator.writerow(values)
    file_handler.close()

def saveResults(fileName,results,user_hash):
     file_handler=open("../../static/res/"+user_hash+".csv","a")
     csv_iterator=csv.writer(file_handler)
     csv_iterator.writerow(["Test results of file with the name: " +fileName])
     for row in results:
          csv_iterator.writerow(row)
     file_handler.close()



@app.post("/api/construct/{user_hash}",status_code=201)
def construct_Controller(user_hash:str,network:network_settings):
    new_network=neural_Network(network.layers,network.mode,network.activationFunction)
    user_map[user_hash]=new_network
    return "added successfully"

@app.post("/api/train/{user_hash}",status_code=200)
def train_Controller(user_hash:str,accuracy:Annotated[str,Form()],max_iterations:Annotated[str,Form()],learning_rate:Annotated[str,Form()],training_file:UploadFile):
    user_network=user_map.get(user_hash)
    training_size=user_network.getNetworkTrainingSize()
    training_set=processFile(training_file.file,training_size[0]+training_size[1])
    batchData, labels = toNumpyArray(training_size[0], training_set)
    user_network.batch_gradient_descent(float(learning_rate),batchData,labels,float(accuracy),float(max_iterations))
    saveParams(user_hash,user_network)

@app.post("/api/test/{user_hash}",status_code=200)    
def test_controller(user_hash:str,testing_file:UploadFile):
    user_network=user_map.get(user_hash)
    network_size=user_network.getNetworkTrainingSize()
    test_set_str=processFile(testing_file.file,network_size[0])
    test_set=toNumpyArray(network_size[0],test_set_str)
    results=user_network.test(test_set[0])
    saveResults(testing_file.filename,results,user_hash)
   