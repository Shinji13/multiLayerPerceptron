export function drawCircle(context,x,y,raduis,color){
    context.beginPath()
    context.fillStyle=color
    context.arc(x,y,raduis,0,2*Math.PI)
    context.fill()
}
export function drawLine(context,start,end,color,lineWidth){
    context.beginPath()
    context.lineWidth=lineWidth
    context.strokeStyle=color
    context.moveTo(start.x,start.y)
    context.lineTo(end.x,end.y)
    context.stroke()
}

export function writeText(context,text,x,y,color,font){
    context.font=font
    context.fillStyle=color
    context.fillText(text,x,y)
}

export function randomColor(colorArray){
    let randomIndex=Math.floor(Math.random()*colorArray.length)
    return colorArray[randomIndex]
}

export function calculateNeuronRadius(canvasHeight,numberOfNeurons){
   return Math.min((12*(canvasHeight/numberOfNeurons))/(586/10),20)
}

export function calculateTextSize(canvasHeight,numberOfNeurons){
   return Math.min((16*(canvasHeight/numberOfNeurons))/(586/10),18)
}

export function delayToDrawNeuron(settings){
      let currentTime=new Date().getTime()
      let delay=currentTime-settings.lastAnimateTime
      if(delay<settings.duration)return false
      settings.lastAnimateTime=currentTime
      return true      
}
