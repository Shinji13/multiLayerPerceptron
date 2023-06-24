from typing import Annotated
from fastapi import FastAPI,HTTPException,Form,UploadFile
from pydantic import BaseModel
from  neuralNetworkConstructure import neural_Network

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
async def train_Controller(user_hash:str,accuracy:Annotated[str,Form()],max_iterations:Annotated[str,Form()],training_file:UploadFile):
    content=await training_file.read()
    print(max_iterations,content,accuracy)