<script>
	import { networkStructure } from '../utils/svelteStore';
	let neuronsNumber = 1;
	let strokeColor = '#ffffff';
	let lineColorFrom = '#000000';
	let lineColorTo = '#ffffff';
</script>

<div id="layers">
	<h2>Customise Network layers</h2>
	<div>
		<span>Remove Layer</span>
		<select
			name="remove"
			id="remove"
			on:change={(evt) => {
				networkStructure.update((prev) => {
					if (networkStructure.length == 1) {
						prev.pop();
					} else {
						prev.splice(evt.currentTarget.value, 1);
					}
					return prev;
				});
				evt.currentTarget.value = -1;
			}}
		>
			<option value={-1} disabled selected>Select a layer</option>
			{#each $networkStructure as layer, index}
				<option value={index}>{index + 1}</option>
			{/each}
		</select>
	</div>
	<div>
		<span>New Layer</span>
		<div>
			<div>
				<span>Neurons number</span>
				<input name="neuronNumber" type="number" bind:value={neuronsNumber} class="number" />
			</div>
			<div>
				<span>Stroke color</span>
				<input id="strokeColor" type="color" bind:value={strokeColor} class="color" />
			</div>
			<div>
				<span>Line first color</span>

				<input id="EdgeColorOne" type="color" bind:value={lineColorFrom} class="color" />
			</div>
			<div>
				<span>Line second color</span>
				<input id="EdgeColorTwo" type="color" bind:value={lineColorTo} class="color" />
			</div>
			<button
				on:click={() => {
					if ($networkStructure.length < 8) {
						let newLayer = {
							color: '#161616',
							neuronsNumber: Math.min(50, Math.max(1, neuronsNumber)),
							strokeColor: strokeColor,
							lineColors: [lineColorFrom, lineColorTo]
						};
						networkStructure.update((prev) => {
							prev.push(newLayer);
							return prev;
						});
					}
				}}>Add</button
			>
		</div>
	</div>
</div>

<style>
	#layers {
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 10px;

		& div {
			display: flex;
			width: 95%;
		}

		& h2 {
			color: var(--primary-color);
			font-family: 'Montserrat', sans-serif;
			font-size: var(--font-sizeMedium);
			font-weight: bold;
		}

		& > div:first-of-type {
			display: flex;
			align-items: center;
			gap: 20px;
			margin-left: 20px;

			& span {
				color: var(--secondary-color);
				font-family: 'Montserrat', sans-serif;
				font-size: var(--font-sizeRegular);
				font-weight: bold;
			}
			& select {
				box-sizing: content-box;
				width: fit-content;
				height: fit-content;
				padding-inline: 1.4rem;
				padding-block: 0.2rem;
				border-radius: 24px;
				border: 2px solid var(--network-color);
				cursor: pointer;
				color: var(--primary-color);
				background-color: transparent;
				font-weight: 600;
				font-family: 'Source Sans Pro', sans-serif;
				font-size: var(--font-sizeSmall);
				position: relative;
				outline: none;

				& option:first-child {
					display: none;
				}

				& option {
					color: black;
				}
			}
		}

		& > div:last-child {
			flex-direction: column;
			gap: 20px;
			margin-left: 20px;

			& > span {
				color: var(--secondary-color);
				font-family: 'Montserrat', sans-serif;
				font-size: var(--font-sizeRegular);
				font-weight: bold;
			}
			& > div {
				flex-direction: column;
				gap: 10px;

				& div {
					align-items: center;
					margin-left: 10px;
					overflow: hidden;
					justify-content: space-between;

					& span {
						color: var(--primary-color);
						font-family: 'Montserrat', sans-serif;
						font-size: var(--font-sizeSmall);
					}

					& .number {
						width: 4rem;
						background-color: transparent;
						border: none;
						border-bottom: 2px solid var(--secondary-color);
						color: var(--primary-color);
						outline: none;
						padding-left: 0.2rem;
						&::-webkit-outer-spin-button,
						&::-webkit-inner-spin-button {
							-webkit-appearance: none;
						}
					}

					& .color {
						width: 3rem;
						height: 3rem;
						border-radius: 50%;
						border: none;
						background-color: transparent;
						border: 2px solid var(--primary-color);
						padding: 2px;

						&::-webkit-color-swatch {
							border: 1px solid var(--primary-color);
							border-radius: 50%;
						}
					}
				}
			}
		}
	}
</style>
