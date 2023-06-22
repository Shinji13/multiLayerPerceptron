import { writable } from 'svelte/store';

export const networkStructure = new writable([
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
		strokeColor: 'white',
		lineColors: ['#bbc3ff', '#1352b8']
	}
]);

export const networkParameters = new writable({
	activationFunction: 0,
	mode: 0
});
