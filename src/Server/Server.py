from typing import Annotated
from fastapi import FastAPI,HTTPException,Form,UploadFile
from pydantic import BaseModel
import numpy as np
from  neuralNetworkConstructure import neural_Network
import csv
import codecs

user_map={}


class network_settings(BaseModel):
    mode:int
    activationFunction:int
    layers:list

app=FastAPI()


@app.get("/")
def get():
    return "ji"

@app.post("/api/construct/{user_hash}",status_code=201)
def construct_Controller(user_hash:str,network:network_settings):
    new_network=neural_Network(network.layers,network.mode,network.activationFunction)
    user_map[user_hash]=new_network
    return "added successfully"

@app.post("/api/train/{user_hash}",status_code=200)
async def train_Controller(user_hash:str,accuracy:Annotated[str,Form()],max_iterations:Annotated[str,Form()],learning_rate:Annotated[str,Form()],training_file:UploadFile):
    file_iterator=codecs.iterdecode(training_file.file,"utf-8")
    csv_iterator=csv.reader(file_iterator,delimiter=",")
    user_network=user_map.get(user_hash)
    training_size=user_network.getNetworkTrainingSize()
    training_list=[]
    for row in csv_iterator:
        if (training_size[0] + training_size[1]) != len(row):
               raise  HTTPException(status_code=400,detail="The training file doesnt match the network")
        training_list.append(row)    
    training_file.file.close()
    string_arr = np.array(training_list)
    float_list = string_arr.astype(float)
    print(float_list)
    batchData=float_list[:,0:training_size[0]]
    labels=float_list[:,training_size[0]:]
    user_network.batch_gradient_descent(learning_rate,batchData,labels,accuracy,max_iterations)

   