<script>
	import AddLayer from '../../components/addLayer.svelte';
	import NetworkConstructor from '../../components/networkConstructor.svelte';
	import WorkspaceParm from '../../components/workspaceParm.svelte';
	import { networkStructure } from '../../utils/svelteStore';
</script>

<div id="workspace">
	<h1>Create your neural network</h1>
	<div>
		<div>
			{#key $networkStructure}
				<NetworkConstructor
					networkLayers={$networkStructure}
					duration={950}
					arrowAnimationSteps={40}
				/>
			{/key}
		</div>
		<AddLayer />
	</div>
	<WorkspaceParm />
</div>

<style>
	#workspace {
		width: 100vw;
		height: 100vh;
		display: flex;
		flex-direction: column;
		padding-top: 5vh;
		padding-left: 3vw;
		gap: 30px;
		background-color: var(--bg-color);

		& > h1 {
			color: var(--primary-color);
			font-family: 'Montserrat', sans-serif;
			font-size: var(--font-sizeBig);
			font-weight: bolder;
		}

		& div:nth-child(2) {
			width: 100%;
			height: 65%;
			display: grid;
			grid-template-columns: 65% 35%;

			& div {
				width: 100%;
				height: 100%;
				overflow-y: hidden;
			}
		}
	}
</style>
