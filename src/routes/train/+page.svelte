<script>
	import NetworkConstructor from '../../components/networkConstructor.svelte';
	import { networkStructure } from '../../utils/svelteStore';
	import { goto } from '$app/navigation';
	import { user_id } from '../../utils/svelteStore';
	import axios from 'axios';
	import Loading from '../../components/loading.svelte';
	let max_iter = 1000;
	let accuarcy = 0.0001;
	let trainingFile = null;
	let learning_rate = 0.1;
	let loading = false;
	let errorMessage = '';

	const handleTrain = async () => {
		if (trainingFile == null) return;
		let formData = new FormData();
		accuarcy = Math.max(0.00001, Math.min(0.1, accuarcy));
		max_iter = Math.min(100000, max_iter);
		learning_rate = Math.min(1, Math.max(0.00000000001, learning_rate));
		formData.append('max_iterations', max_iter.toString());
		formData.append('accuracy', accuarcy.toString());
		formData.append('learning_rate', learning_rate.toString());
		formData.append('training_file', trainingFile);
		loading = true;
		await axios
			.post(`/api/train/${$user_id}`, formData, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			})
			.then(() => {
				loading = false;
				goto('/test');
			})
			.catch((err) => {
				loading = false;
				if (err.response.status == 400)
					errorMessage = `Invalid training data it should be in form of n row and ${
						$networkStructure[0].neuronsNumber + $networkStructure.at(-1).neuronsNumber
					} columns first ${
						$networkStructure[0].neuronsNumber
					} represent neural network input and the rest is its output ordered from top to bottom.`;
			});
	};
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
			<span>Learning rate</span>
			<input type="number" bind:value={learning_rate} />
		</div>
		<div>
			<label for="training_set"
				>{trainingFile != null ? trainingFile.name : 'Upload training data'}</label
			>
			<input
				id="training_set"
				type="file"
				accept=".csv"
				on:change={(evt) => {
					trainingFile = evt.target.files[0];
				}}
			/>
		</div>
		<button on:click={handleTrain}>Train</button>
	</section>
	<section>
		{#if loading}
			<Loading />
		{:else if errorMessage == ''}
			<span
				>--Accuracy represent the difference between two consecutive losses when we reach its value
				we stop the training.</span
			>
			<span
				>--Max number of iterations is needed in case we don't converage to the accuracy point.</span
			>
			<span
				>--The training file need to be in csv format and contains row of samples with both inputs
				and labels also it can't bypass 8mb.</span
			>
			<span
				>--Learning rate needs to be between 0 and 1 and it represents how big the step of gradient
				descent .</span
			>
		{:else}
			<span class="error">{errorMessage}</span>
		{/if}
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
			height: 58%;
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
				font-family: 'Source Sans Pro', sans-serif;
				font-weight: 400;
				font-size: var(--font-sizeSmall);
			}

			& .error {
				color: rgba(194, 17, 17, 0.925);
			}
		}
	}
</style>
