<script>
	import NetworkConstructor from '../../components/networkConstructor.svelte';
	import Loading from '../../components/loading.svelte';
	import axios from 'axios';
	import { networkStructure, user_id } from '../../utils/svelteStore';
	import { goto } from '$app/navigation';

	let test_name = 'Xi';
	let test_file = null;
	let loading = false;
	let errorMessage = '';

	const handleTest = async () => {
		let fd = new FormData();
		fd.append('testing_file', test_file);
		loading = true;
		await axios
			.post(`/api/test/${$user_id}`, fd, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			})
			.then(() => {
				loading = false;
			})
			.catch((err) => {
				loading = false;
				if (err.response.status == 400)
					errorMessage = `Invalid test data it should be in form of n row and ${$networkStructure[0].neuronsNumber} columns`;
			});
	};
</script>

<!-- svelte-ignore missing-declaration -->
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
			<span>Current testing name</span>
			<input type="text" bind:value={test_name} />
		</div>
		<div>
			<label for="resualts">Download resualts</label>
			<input id="resualts" type="file" />
		</div>
		<div>
			<label for="testing_set">{test_file != null ? test_file.name : 'Upload test data'}</label>
			<input
				id="testing_set"
				type="file"
				accept=".csv"
				on:change={(evt) => {
					test_file = evt.target.files[0];
				}}
			/>
		</div>
		<button on:click={handleTest}>Test</button>
	</section>
	<section>
		{#if loading}
			<Loading />
		{:else if errorMessage == ''}
			<span
				>--Results are weights and biases of the network after the training along side the outcome
				of testing samples if any exist all.</span
			>
			<span
				>--The testing file need to contain rows of testing samples where each one contain the
				values of input layer neurons</span
			>
		{:else}
			<span class="error">{errorMessage}</span>
		{/if}
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
			& div:first-child {
				& input {
					display: inline-block;
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
		}
	}
</style>
