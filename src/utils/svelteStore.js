import { readable, writable } from 'svelte/store';
import { nanoid } from 'nanoid';

export const networkStructure = new writable([
	{
		color: '#161616',
		neuronsNumber: 2,
		strokeColor: 'white',
		lineColors: ['#612458', 'white']
	},
	{
		color: '#161616',
		neuronsNumber: 2,
		strokeColor: 'white',
		lineColors: ['#bbc3ff', '#1352b8']
	},
	{
		color: '#161616',
		neuronsNumber: 1,
		strokeColor: 'white',
		lineColors: ['#bbc3ff', '#1352b8']
	}
]);

export const user_id = new readable(nanoid());
