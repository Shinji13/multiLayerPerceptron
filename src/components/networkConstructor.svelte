<script>
  	import { onMount } from "svelte";
    import {drawCircle,drawLine,writeText,calculateNeuronRadius, delayToDrawNeuron, calculateTextSize}  from "../utils/canvasMethods"    
    
    export let networkLayers=[{color:"red",neuronsNumber:10,values:[1,3,1.4,3.5,2.3]},{color:"blue",neuronsNumber:5,values:[2,3,3.4,3.5,2.7]},{color:"gray",neuronsNumber:3,values:[1,3,1.4,3.5,2.3]}]
    export let edgeColor="white"

    let settings={
         canvas:null,
         context:null,                   
         lastAnimateTime:0,
         arrowAnimationSteps:50,
         duration:250,
    }
    let edgesPositions =[]
    let currentDrawnLayer=0
    let currentDrawnNeuron=0    

    onMount(()=>{            
      settings.lastAnimateTime=new Date().getTime()    
      settings.canvas.width = settings.canvas.offsetWidth
      settings.canvas.height = settings.canvas.offsetHeight
      settings.context=settings.canvas.getContext("2d")
      let layerWidth=settings.canvas.width/networkLayers.length
      networkLayers=networkLayers.map((layer,index)=>{
           let startingX=layerWidth*index+layerWidth/2
           let radius=calculateNeuronRadius(settings.canvas.height,layer.neuronsNumber)
           let heightSpacing=(settings.canvas.height-layer.neuronsNumber*radius)/(layer.neuronsNumber+1)
           let currentHeight=heightSpacing
           let neuronsPositions=[]
           for ( let i=0; i<layer.neuronsNumber; i++){
                neuronsPositions.push({x:startingX,y:currentHeight+radius/2})                
                currentHeight+=heightSpacing+radius
           }
           return {            
             ...layer,
             neuronsPositions            
           }
      })    
      draw()
    })
 

    export function onResize(){
      settings.canvas.width = settings.canvas.offsetWidth
      settings.canvas.height = settings.canvas.offsetHeight
      animate()
    }

    export function animate(){
      settings.context.clearRect(0, 0, settings.canvas.width, settings.canvas.height);
      currentDrawnLayer=0
      currentDrawnNeuron=0
      draw()
    }

    function draw(){
       if(edgesPositions.length==0 ){
         if(currentDrawnLayer == networkLayers.length) return 
         if(delayToDrawNeuron(settings))
            drawNeurons()
      }
      else{
          drawEges()          
      }       
      requestAnimationFrame(draw)
    }

    function drawEges(){
        let targetX=networkLayers[currentDrawnLayer-1].neuronsPositions[0].x
        if(targetX-edgesPositions[0][0].x<0.0000000001){
              edgesPositions.length=0                                     
        }
        edgesPositions.forEach((neuronWeights,index)=>{         
            let start=networkLayers[currentDrawnLayer-2].neuronsPositions[index]
            for(let i=0;i<neuronWeights.length;i++){
              let target=networkLayers[currentDrawnLayer-1].neuronsPositions[i]
              drawLine(settings.context,start,neuronWeights[i],edgeColor,1.5)
              let deltaX=(target.x-start.x)/settings.arrowAnimationSteps
              let deltaY=(target.y-start.y)/settings.arrowAnimationSteps
              neuronWeights[i].x+=deltaX
              neuronWeights[i].y+=deltaY              
            }
        })
        
    }

    function drawNeurons(){
      let layerIndex=currentDrawnLayer
      let layer=networkLayers[layerIndex]
      let currentNeuronPosition=layer.neuronsPositions[currentDrawnNeuron]
      let radius=calculateNeuronRadius(settings.canvas.height,layer.neuronsNumber)
      let fontSize=calculateTextSize(settings.canvas.height,layer.neuronsNumber)
      drawCircle(settings.context,currentNeuronPosition.x,currentNeuronPosition.y,radius,layer.color)            
      writeText(settings.context,layer.values[currentDrawnNeuron],currentNeuronPosition.x-radius,currentNeuronPosition.y-radius-5,"white",`${fontSize}px sans-serif`)  
      currentDrawnNeuron+=1
      if(currentDrawnNeuron==layer.neuronsNumber){
        currentDrawnLayer+=1
        currentDrawnNeuron=0  
      }
      if(currentDrawnLayer-2>=0){
          let startingLayerNeurons=networkLayers[layerIndex-1].neuronsNumber
          let endingLayerNeurons=networkLayers[layerIndex].neuronsNumber
          for (let i=0;i<startingLayerNeurons;i++){
             let currentWeights=[]
             let currentNeuron=networkLayers[layerIndex-1].neuronsPositions[i]
             for(let j=0;j<endingLayerNeurons;j++)currentWeights.push({...currentNeuron})
             edgesPositions.push(currentWeights)
          }
      }
  }
</script>

<canvas bind:this={settings.canvas} id="canvas"/>


<style>
  #canvas{
    width: 100%;
    height:100%;
    background-color: black;
  }
</style>