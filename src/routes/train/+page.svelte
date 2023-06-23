<script>
	import NetworkConstructor from '../../components/networkConstructor.svelte';
	import { networkStructure } from '../../utils/svelteStore';
	import { goto } from '$app/navigation';
	let max_iter = 10000;
	let accuarcy = 0.0001;
</script>

<div id="train">
	<section>
		<h1>Train your network</h1>
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<i class="fa-solid fa-arrow-left" style="color: #ffffff;" on:click={() => goto('/construct')} />
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
			<span>maximum iterations</span>
			<input type="number" bind:value={max_iter} />
		</div>
		<div>
			<span>Accuarcy</span>
			<input type="number" bind:value={accuarcy} />
		</div>
		<div>
			<label for="training_set">Upload training data</label>
			<input id="training_set" type="file" />
		</div>
		<button
			on:click={() => {
				// check inputs
				// send the req
				// w8 for res
				goto('/test');
			}}>Train</button
		>
	</section>
	<section>
		<span
			>--Accuracy represent the difference between two consecutive losses the lower this value gets
			the slower training go.</span
		>
		<span
			>--Max number of iterations is needed in case we don't converage to the accuracy point.</span
		>
		<span
			>--The training file need to be in csv format and contains row of samples with both inputs and
			labels also it can't bypass 8mb.</span
		>
	</section>
</div>

<style>
	#train {
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

			& div:last-of-type {
				& input {
					display: none;
				}
				& label {
					color: var(--primary-color);
					background-color: var(--secondary-color);
					font-family: 'Montserrat', sans-serif;
					font-size: var(--font-sizeRegular);
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
