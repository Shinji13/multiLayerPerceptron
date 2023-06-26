<script>
</script>

<section id="loading">
	<span>
		<span />
	</span>
	<span>Loading...</span>
</section>

<style>
	@keyframes rotate {
		0% {
			rotate: 0deg;
		}
		100% {
			rotate: 360deg;
		}
	}

	@keyframes appear {
		0% {
			opacity: 1;
		}
		50% {
			opacity: 0;
		}
		100% {
			opacity: 1;
		}
	}

	#loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;

		& span {
			overflow: hidden;
		}

		& span:first-child {
			aspect-ratio: 1/1;
			border-radius: 50%;
			background-color: transparent;
			border: 3px solid var(--secondary-color);
			animation: rotate 1800ms linear 0s infinite normal forwards;
		}

		& > span:first-child {
			display: flex;
			justify-content: center;
			align-items: center;
			border-left: none;
			border-top: none;
			width: 3rem;

			& span {
				border-right: none;
				border-bottom: none;
				width: 2.5rem;
			}
		}

		& > span:last-child {
			color: var(--primary-color);
			font-family: 'Montserrat', sans-serif;
			font-size: var(--font-sizeMedium);
			font-weight: 600;
			animation: appear 1800ms linear 0s infinite forwards normal;
		}
	}
</style>
