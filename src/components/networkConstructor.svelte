<script>
	import { onMount } from "svelte";
    import {drawCircle,drawLine,writeText,calculateNeuronRadius}  from "../utils/canvasMethods"    
    export let networkLayers=[{color:"red",neuronsNumber:5,values:[1,3,1.4,3.5,2.3]},{color:"blue",neuronsNumber:5,values:[2,3,3.4,3.5,2.7]},{color:"gray",neuronsNumber:3,values:[1,3,1.4,3.5,2.3]}]
    export let canvasWidth=0
    export let canvasHeight=0  

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
      settings.canvas.width=canvasWidth    
      settings.canvas.height=canvasHeight
      settings.context=settings.canvas.getContext("2d")
      let layerWidth=canvasWidth/networkLayers.length
      networkLayers=networkLayers.map((layer,index)=>{
           let startingX=layerWidth*index+layerWidth/2
           let neuronRaduis=calculateNeuronRadius(canvasHeight,layer.neuronsNumber)
           let heightSpacing=(settings.canvas.height-layer.neuronsNumber*neuronRaduis)/(layer.neuronsNumber+1)
           let currentHeight=heightSpacing
           let neuronsPositions=[]
           for ( let i=0; i<layerLength; i++){
                neuronsPositions.push({x:startingX,y:currentHeight+10})                
                currentHeight+=heightSpacing+20
           }
           return {            
             ...layer,
             neuronsPositions            
           }
      })    
      draw()
    })

    function draw(){
       if(edgesPositions.length==0){
         let currentTime=new Date().getTime()
         let delay=currentTime-settings.lastAnimateTime
         if(delay>=settings.duration){
           settings.lastAnimateTime=currentTime
           drawNeurons()
         }
      }
      else{
          drawEges()
      }
      requestAnimationFrame(draw)
    }

    function drawEges(){
        let targetX=networkLayers[currentDrawnLayer-1].neuronsPositions[0].x
        if(targetX-edgesPositions[0][0].x<0.0000000001)
             edgesPositions.length=0                         
        edgesPositions.forEach((neuronWeights,index)=>{         
            let start=networkLayers[currentDrawnLayer-2].neuronsPositions[index]
            for(let i=0;i<neuronWeights.length;i++){
              let target=networkLayers[currentDrawnLayer-1].neuronsPositions[i]
              drawLine(settings.context,start,neuronWeights[i],"white",1.5)
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
      let radius=calculateNeuronRadius(canvasHeight,layer.neuronsNumber)
      drawCircle(settings.context,currentNeuronPosition.x,currentNeuronPosition.y,radius,layer.color)        
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