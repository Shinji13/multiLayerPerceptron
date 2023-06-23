<script>
	import { networkParameters, networkStructure } from '../utils/svelteStore';
	import { goto } from '$app/navigation';

	let activationFunction = 0;
	let mode = 0;
</script>

<div id="params">
	<h2>Neural network parameters</h2>
	<div>
		<div>
			<span>Activation function</span>
			<select name="activation" id="activation" bind:value={activationFunction}>
				<option value={0}>ReLu</option>
				<option value={1}>SoftPlus</option>
			</select>
		</div>
		<div>
			<span>Operation mode</span>
			<select name="mode" id="mode" bind:value={mode}>
				<option value={0}>Regression</option>
				<option value={1}>multiClass Classification</option>
				<option value={2}>multiLable Classification</option>
			</select>
		</div>
		<button
			on:click={() => {
				if (mode == 0) {
					let lastLayer = $networkStructure.length - 1;
					$networkStructure[lastLayer].neuronsNumber = 1;
				}
				networkParameters.set({
					activationFunction,
					mode
				});
				// send post request to create the network
				goto('/train');
			}}>Create</button
		>
	</div>
</div>

<style>
	#params {
		display: flex;
		flex-direction: column;
		width: 100%;
		gap: 20px;

		& h2 {
			color: var(--primary-color);
			font-family: 'Montserrat', sans-serif;
			font-size: var(--font-sizeMedium);
			font-weight: bolder;
		}

		& > div {
			display: flex;
			align-items: center;
			gap: 8vw;
			padding-left: 2vw;

			& div {
				display: flex;
				align-items: center;
				gap: 20px;

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
					padding-inline: 0.5rem;
					padding-block: 0.3rem;
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

					& option {
						color: black;
					}
				}
			}
		}
	}
</style>
