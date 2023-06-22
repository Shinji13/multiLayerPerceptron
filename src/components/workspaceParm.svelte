<script>
	import { networkParameters } from '../utils/svelteStore';
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
				networkParameters.set({
					activationFunction,
					mode
				});
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

			& button {
				width: fit-content;
				height: fit-content;
				padding-block: 0.3rem;
				padding-inline: 2.5rem;
				display: flex;
				align-items: center;
				justify-content: space-evenly;
				position: relative;
				font-family: 'Source Sans Pro', sans-serif;
				font-size: var(--font-sizeRegular);
				font-weight: bold;
				z-index: 2;
				cursor: pointer;
				color: var(--primary-color);
				background-color: transparent;
				border-radius: 24px;
				border: 2px solid var(--network-color);
				overflow: hidden;

				&:hover {
					& i {
						color: var(--network-color);
					}
					border-color: var(--network-color);
					color: var(--network-color);
					&::before {
						width: 100%;
					}
				}
				&::before {
					content: '';
					display: inline-block;
					width: 0;
					height: 100%;
					position: absolute;
					left: 0;
					top: 0;
					transition: all 300ms 0s ease;
					background-color: var(--primary-color);
					border-radius: 0.5px;
					z-index: -1;
				}
			}

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
