<script>
	import NetworkConstructor from './networkConstructor.svelte';
	import { goto } from '$app/navigation';
</script>

<div id="home">
	<div class="navbar">
		<div class="logo" />
	</div>
	<div class="body">
		<div class="left-side">
			<h1>Build Neuron Networks Easily</h1>
			<p>
				construct neuron networks with custom settings and then train them with csv files to get
				appropriate weights
			</p>
			<button
				on:click={() => {
					goto('/construct');
				}}>Get Started <i class="fa-solid fa-arrow-right" /></button
			>
		</div>
		<div class="right-side">
			<NetworkConstructor duration={150} arrowAnimationSteps={40} />
		</div>
	</div>
</div>

<style>
	@keyframes coloring {
		0% {
			background-position: 0 center;
		}
		100% {
			background-position: -200% center;
		}
	}

	#home {
		width: 100vw;
		height: 100vh;
		background-color: var(--bg-color);
		display: flex;
		flex-direction: column;
		gap: 12vh;

		& > .navbar {
			width: 100%;
			height: 60px;
			display: flex;
			align-items: center;
			justify-content: space-between;

			& > .sections {
				display: flex;
				align-items: center;
				font-family: 'Source Sans Pro', sans-serif;
				font-weight: 400;
				font-size: var(--font-sizeRegular);
				color: var(--text-color);
				margin-right: 10vw;
				gap: 5vw;

				& ul {
					display: flex;
					align-items: center;
					gap: 16px;

					& li {
						cursor: pointer;
					}

					& li:hover {
						color: var(--primary-color);
					}
				}

				& button {
					width: 8rem;
					height: 2.5rem;
					display: flex;
					align-items: center;
					letter-spacing: 0.5px;
					justify-content: center;
					position: relative;
					font-family: 'Source Sans Pro', sans-serif;
					font-size: var(--font-sizeRegular);
					font-weight: bold;
					color: var(--primary-color);
					cursor: pointer;
					z-index: 2;
					padding-inline: 0.2rem;
					padding-block: 0.2rem;
					background: linear-gradient(
						to right,
						var(--secondary-color),
						rgb(12, 78, 199),
						var(--primary-color)
					);
					border-radius: 4px;
					border: none;
					&:hover {
						background: linear-gradient(
							to right,
							var(--primary-color),
							rgb(204, 217, 245),
							var(--secondary-color)
						);
						color: var(--secondary-color);
					}
				}
			}

			& .logo {
				width: 220px;
				height: 50px;
				margin-left: 2vw;
				background-image: url('/images/logo.png');
				background-repeat: no-repeat;
				background-position: center;
				background-size: cover;
			}
		}

		& .body {
			width: 100%;
			display: grid;
			grid-template-columns: 45% 55%;
			align-items: center;
			justify-content: center;

			& .right-side {
				width: 100%;
				height: 65vh;
				overflow: hidden;
			}

			& .left-side {
				margin-left: 2vw;
				width: 100%;
				display: flex;
				flex-direction: column;
				gap: 25px;

				& h1 {
					font-family: 'Montserrat', sans-serif;
					font-size: var(--font-sizeXXl);
					font-weight: bolder;
					background: linear-gradient(
						to right,
						var(--secondary-color),
						var(--text-color),
						var(--primary-color),
						var(--secondary-color)
					);
					background-size: 200%;
					background-clip: text;
					animation: coloring 3s ease-in-out 0.5s infinite normal forwards;
					color: transparent;
					letter-spacing: 3px;
				}

				& p {
					color: var(--text-color);
					font-family: 'Source Sans Pro', sans-serif;
					font-size: var(--font-sizeRegular);
					font-weight: 400;
				}
			}
		}
		& button {
			gap: 40px;
			padding-inline: 1rem;
			padding-block: 0.5rem;
		}
	}
</style>
