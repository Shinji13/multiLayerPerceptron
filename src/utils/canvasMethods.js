export function drawCircle(context, x, y, raduis, color) {
	context.beginPath();
	context.fillStyle = color;
	context.arc(x, y, raduis, 0, 2 * Math.PI);
	context.fill();
}

export function drawArc(context, x, y, raduis, color, start, end, lineWidth) {
	context.beginPath();
	context.lineWidth = lineWidth;
	context.strokeStyle = color;
	context.arc(x, y, raduis, start, end);
	context.stroke();
}

export function drawLine(context, start, end, color, lineWidth) {
	context.beginPath();
	context.lineWidth = lineWidth;
	context.strokeStyle = color;
	context.moveTo(start.x, start.y);
	context.lineTo(end.x, end.y);
	context.stroke();
}

export function writeText(context, text, x, y, color, font) {
	context.font = font;
	context.fillStyle = color;
	context.fillText(text, x, y);
}

export function randomColor(colorArray) {
	let randomIndex = Math.floor(Math.random() * colorArray.length);
	return colorArray[randomIndex];
}

export function calculateNeuronRadius(canvasHeight, numberOfNeurons) {
	return Math.min((12 * (canvasHeight / numberOfNeurons)) / (586 / 10), 20);
}

export function calculateTextSize(canvasHeight, numberOfNeurons) {
	return Math.min((16 * (canvasHeight / numberOfNeurons)) / (586 / 10), 18);
}

export function delayToDrawNeuron(duration, settings, layerNeuronNumber) {
	let currentTime = new Date().getTime();
	let delay = currentTime - settings.lastAnimateTime;
	if (delay < duration / layerNeuronNumber) return false;
	settings.lastAnimateTime = currentTime;
	return true;
}

export function createGradient(context, arrayOfColors, start, end) {
	const gradient = context.createLinearGradient(start.x, start.y, end.x, end.y);
	for (let i = 0; i < arrayOfColors.length; i++)
		gradient.addColorStop(i / arrayOfColors.length, arrayOfColors[i]);
	return gradient;
}
