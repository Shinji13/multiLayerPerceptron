<script>
  import { onMount } from "svelte";
  import {drawCircle,drawLine,writeText,randomColor}  from "../utils/canvasMethods"

  let colors = [
    "#EB5757",
    "#4AC29A",
    "#B2FEFA",
    "#D66D75",
    "#E44D26",
    "#20002c",
    "#C33764",
    "#34e89e",
    "#6190E8",
    "#A7BFE8",
    "#0575E6",
    "#4568DC",
    "#643843",
    "#99627A",
    "#C88EA7",
    "#116D6E",
    "#CD1818",
  ];
  const settings={
    networkLayers:[5,10,5],
    canvas:null,
    context:null,    
    networkNeurons:[],
    lastAnimateTime:0,
    duration:550
  }
  let currentDrawnNeuron={
    layer:0,
    neuronIndex:0
  } 
  let weightsPositions =[]
  onMount(()=>{
      settings.lastAnimateTime=new Date().getTime()
      settings.canvas.width=window.innerWidth*0.9
      settings.canvas.height=window.innerHeight*0.9
      settings.context=settings.canvas.getContext("2d")
      let layerWidth=settings.canvas.width/settings.networkLayers.length
      settings.networkNeurons=settings.networkLayers.map((layerLength,index)=>{
           let startingX=layerWidth*index+layerWidth/2
           let heightSpacing=(settings.canvas.height-layerLength*20)/(layerLength+1)
           let currentHeight=heightSpacing
           let currentLayerNeurons=[]
           for ( let i=0; i<layerLength; i++){
                currentLayerNeurons.push({x:startingX,y:currentHeight+10})                
                currentHeight+=heightSpacing+20
           }
           return currentLayerNeurons
      })    
      draw()
  })
  function draw(){
      if(weightsPositions.length==0){
         let currentTime=new Date().getTime()
         let delay=currentTime-settings.lastAnimateTime
         if(delay>=settings.duration){
           settings.duration-=68
           settings.lastAnimateTime=currentTime
           drawNeurons()
         }
      }
      else{      
        let targetX=settings.networkNeurons[currentDrawnNeuron.layer-1][0].x
        if(targetX-weightsPositions[0][0].x<0.0000000001){
             weightsPositions.length=0             
             settings.duration=550
        }
        weightsPositions.forEach((neuronWeights,index)=>{         
            let start=settings.networkNeurons[currentDrawnNeuron.layer-2][index]
            for(let i=0;i<neuronWeights.length;i++){
              let target=settings.networkNeurons[currentDrawnNeuron.layer-1][i]
              drawLine(settings.context,start,neuronWeights[i],"white",1.5)
              let deltaX=(target.x-start.x)/48
              let deltaY=(target.y-start.y)/48
              neuronWeights[i].x+=deltaX
              neuronWeights[i].y+=deltaY              
            }
        })
      }
      requestAnimationFrame(draw)
  }
  function drawNeurons(){
      let layerIndex=currentDrawnNeuron.layer
      let layer=settings.networkNeurons[layerIndex]
      let currentNeuronPosition=layer[currentDrawnNeuron.neuronIndex]
      let color=colors[layerIndex]
      drawCircle(settings.context,currentNeuronPosition.x,currentNeuronPosition.y,20,color)        
      currentDrawnNeuron.neuronIndex+=1
      if(currentDrawnNeuron.neuronIndex==layer.length){
        currentDrawnNeuron.layer+=1
        currentDrawnNeuron.neuronIndex=0  
      }
      if(currentDrawnNeuron.layer-2>=0){
          let startingLayerNeurons=settings.networkLayers[layerIndex-1]
          let endingLayerNeurons=settings.networkLayers[layerIndex]
          for (let i=0;i<startingLayerNeurons;i++){
             let currentWeights=[]
             let currentNeuron=settings.networkNeurons[layerIndex-1][i]
             for(let j=0;j<endingLayerNeurons;j++)currentWeights.push({...currentNeuron})
             weightsPositions.push(currentWeights)
          }
      }
  }
</script>

<canvas id="canvas" bind:this={settings.canvas}/>
<style>
    #canvas{
        width: 90%;
        height: 90%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-50%);
        background-color: black;
        border-radius: 12px;        
    }
</style>