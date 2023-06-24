<script>
	import NetworkConstructor from '../../components/networkConstructor.svelte';
	import { networkStructure } from '../../utils/svelteStore';
	import { goto } from '$app/navigation';
</script>

<div id="test">
	<section>
		<h1>Test your network</h1>
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<i class="fa-solid fa-arrow-left" style="color: #ffffff;" on:click={() => goto('/train')} />
	</section>
	<section>
		<NetworkConstructor
			networkLayers={$networkStructure}
			duration={1200}
			arrowAnimationSteps={35}
		/>
	</section>
	<section>
		<div>
			<label for="resualts">Download training resualts</label>
			<input id="resualts" type="file" />
		</div>
		<div>
			<label for="testing_set">Upload testing data</label>
			<input id="testing_set" type="file" />
		</div>
		<button
			on:click={() => {
				// check inputs
				// send the req
				// w8 for res
			}}>Test</button
		>
	</section>
	<section>
		<span
			>--Training file need to be a csv file where each row respresent a sample of input for the
			network.</span
		>
		<span
			>--The resualts contains the adjusted weights and biases for each layer of your network.</span
		>
	</section>
</div>

<style>
	#test {
		width: 100vw;
		height: 100vh;
		display: flex;
		flex-direction: column;
		padding-top: 20px;
		gap: 20px;
		padding-left: 4vw;
		background-color: var(--bg-color);

		& span {
			color: var(--secondary-color);
			font-family: 'Montserrat', sans-serif;
			font-size: var(--font-sizeRegular);
			font-weight: bold;
		}

		& section {
			width: 100%;
		}

		& section:first-child {
			display: flex;
			align-items: center;
			justify-content: space-between;
			padding-right: 2vw;

			& h1 {
				color: var(--primary-color);
				font-family: 'Montserrat', sans-serif;
				font-size: var(--font-sizeBig);
				font-weight: bolder;
			}

			& i {
				font-size: 2rem;
				width: 3rem;
				aspect-ratio: 1/1;
				display: flex;
				align-items: center;
				justify-content: center;
				cursor: pointer;

				&:hover {
					background-color: var(--secondary-color);
					border-radius: 50%;
				}
			}
		}
		& section:nth-child(2) {
			height: 60%;
			overflow: hidden;
		}
		& section:nth-child(3) {
			display: flex;
			justify-content: space-evenly;
			align-items: center;

			& div {
				& input {
					display: none;
				}
				& label {
					color: var(--primary-color);
					background-color: var(--secondary-color);
					font-family: 'Montserrat', sans-serif;
					font-size: var(--font-sizeSmall);
					font-weight: 600;
					border-radius: 16px;
					padding-block: 0.3rem;
					padding-inline: 1rem;
					cursor: pointer;
				}
			}

			& div {
				display: flex;
				gap: 10px;
			}

			& input {
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
		}
		& section:last-child {
			display: flex;
			flex-direction: column;
			gap: 5px;

			& span {
				color: var(--text-color);
				font-weight: 400;
				font-size: var(--font-sizeSmall);
			}
		}
	}
</style>
