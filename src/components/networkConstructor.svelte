<script>
	import { onMount } from 'svelte';
	import {
		drawCircle,
		drawLine,
		calculateNeuronRadius,
		delayToDrawNeuron,
		writeText,
		calculateTextSize,
		drawArc,
		createGradient
	} from '../utils/canvasMethods';

	export let networkLayers = [
		{
			color: '#161616',
			neuronsNumber: 10,
			strokeColor: 'white',
			lineColors: ['#612458', 'white']
		},
		{
			color: '#161616',
			neuronsNumber: 5,
			strokeColor: 'white',
			lineColors: ['#bbc3ff', '#1352b8']
		},
		{
			color: '#161616',
			neuronsNumber: 3,
			strokeColor: 'white'
		}
	];
	export let arrowAnimationSteps = 40;
	export let duration = 150;

	let settings = {
		canvas: null,
		context: null,
		lastAnimateTime: 0
	};
	let edgesPositions = [];
	let currentDrawnLayer = 0;
	let currentDrawnNeuron = 0;

	onMount(() => {
		settings.lastAnimateTime = new Date().getTime();
		settings.context = settings.canvas.getContext('2d');
		settings.canvas.width = settings.canvas.offsetWidth;
		settings.canvas.height = settings.canvas.offsetHeight;
		let layerWidth = settings.canvas.width / (networkLayers.length * 1.3);
		networkLayers = networkLayers.map((layer, index) => {
			let startingX = layerWidth * index + layerWidth / 2;
			let radius = calculateNeuronRadius(settings.canvas.height, layer.neuronsNumber);
			let heightSpacing =
				(settings.canvas.height - layer.neuronsNumber * radius) / (layer.neuronsNumber + 1);
			let currentHeight = heightSpacing;
			let neuronsPositions = [];
			for (let i = 0; i < layer.neuronsNumber; i++) {
				neuronsPositions.push({ x: startingX, y: currentHeight + radius / 2 });
				currentHeight += heightSpacing + radius;
			}
			return {
				...layer,
				neuronsPositions
			};
		});
		draw();
	});
	export function animate() {
		settings.context.clearRect(0, 0, settings.canvas.width, settings.canvas.height);
		currentDrawnLayer = 0;
		currentDrawnNeuron = 0;
		draw();
	}

	function draw() {
		if (edgesPositions.length == 0) {
			if (currentDrawnLayer == networkLayers.length) return;
			if (delayToDrawNeuron(duration, settings, networkLayers[currentDrawnLayer].neuronsNumber))
				drawNeurons();
		} else {
			drawEges();
		}
		requestAnimationFrame(draw);
	}

	function drawText(currentNeuronPosition, radius) {
		let layer = networkLayers[currentDrawnLayer];
		if (layer.values) {
			let fontSize = calculateTextSize(settings.canvas.height, layer.neuronsNumber);
			writeText(
				settings.context,
				layer.values[currentDrawnNeuron],
				currentNeuronPosition.x - radius,
				currentNeuronPosition.y - radius - 5,
				'white',
				`${fontSize}px sans-serif`
			);
		}
	}

	function drawEges() {
		let targetX = networkLayers[currentDrawnLayer - 1].neuronsPositions[0].x;
		let radius = calculateNeuronRadius(
			settings.canvas.height,
			networkLayers[currentDrawnLayer - 1].neuronsNumber
		);
		if (targetX - edgesPositions[0][0].x <= radius / 1.2) {
			edgesPositions.length = 0;
		}
		edgesPositions.forEach((neuronWeights, index) => {
			let start = networkLayers[currentDrawnLayer - 2].neuronsPositions[index];
			for (let i = 0; i < neuronWeights.length; i++) {
				let target = networkLayers[currentDrawnLayer - 1].neuronsPositions[i];
				let edgeColor = createGradient(
					settings.context,
					networkLayers[currentDrawnLayer - 2].lineColors,
					start,
					neuronWeights[i]
				);
				drawLine(settings.context, start, neuronWeights[i], edgeColor, 1.5);
				let deltaX = (target.x - start.x) / arrowAnimationSteps;
				let deltaY = (target.y - start.y) / arrowAnimationSteps;
				neuronWeights[i].x += deltaX;
				neuronWeights[i].y += deltaY;
			}
		});
	}

	function drawNeurons() {
		let layerIndex = currentDrawnLayer;
		let layer = networkLayers[layerIndex];
		let currentNeuronPosition = layer.neuronsPositions[currentDrawnNeuron];
		let radius = calculateNeuronRadius(settings.canvas.height, layer.neuronsNumber);
		drawText(currentNeuronPosition, radius);
		drawArc(
			settings.context,
			currentNeuronPosition.x,
			currentNeuronPosition.y,
			radius + 2,
			layer.strokeColor,
			0,
			2 * Math.PI,
			4
		);
		drawCircle(
			settings.context,
			currentNeuronPosition.x,
			currentNeuronPosition.y,
			radius,
			layer.color
		);
		currentDrawnNeuron += 1;
		if (currentDrawnNeuron == layer.neuronsNumber) {
			currentDrawnLayer += 1;
			currentDrawnNeuron = 0;
		}
		if (currentDrawnLayer - 2 >= 0) {
			let startingLayerNeurons = networkLayers[layerIndex - 1].neuronsNumber;
			let endingLayerNeurons = networkLayers[layerIndex].neuronsNumber;
			for (let i = 0; i < startingLayerNeurons; i++) {
				let currentWeights = [];
				let currentNeuron = networkLayers[layerIndex - 1].neuronsPositions[i];
				for (let j = 0; j < endingLayerNeurons; j++) currentWeights.push({ ...currentNeuron });
				edgesPositions.push(currentWeights);
			}
		}
	}
</script>

<canvas bind:this={settings.canvas} id="canvas" />

<style>
	#canvas {
		width: 100%;
		height: 100%;
		background-color: transparent;
	}
</style>
