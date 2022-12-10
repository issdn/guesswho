<script lang="ts">
	import { sendTask } from '../socketStore';
	import { onMount } from 'svelte';
	import { gameEndInfo, myGameId, enemyGameId, game } from '../stores';
	import Button from './Button.svelte';
	import { prettifyCharacterName } from '../scripts';
	import TextLoading from './utils/TextLoading.svelte';

	const winner = $gameEndInfo.winner_id === $myGameId;

	let characters = winner ? ['🥳', '🎉', '✨'] : ['😭', '💧', '🕷'];

	/**
	 * Code written by by:
	 * https://svelte.dev/tutorial/congratulations
	 * https://github.com/sveltejs/svelte/commits/master/site/content/tutorial/19-next-steps/01-congratulations
	 * Rich-Harris
	 * Conduitry
	 * BabakFP
	 * alexiglesias93
	 * ramozdev
	 * ignatiusmb
	 * hyp3rflow
	 * benmaccann
	 */
	let confetti = new Array(100)
		.fill()
		.map((_, i) => {
			return {
				character: characters[i % characters.length],
				x: Math.random() * 100,
				y: -20 - Math.random() * 100,
				r: 0.1 + Math.random() * 1
			};
		})
		.sort((a, b) => a.r - b.r);

	let time = 3;
	onMount(() => {
		setInterval(() => {
			if ((time = 0)) return;
			else time--;
		}, 1000);

		let frame: number;

		function loop() {
			frame = requestAnimationFrame(loop);

			confetti = confetti.map((emoji) => {
				emoji.y += 0.7 * emoji.r;
				if (emoji.y > 120) emoji.y = -20;
				return emoji;
			});
		}

		loop();

		return () => cancelAnimationFrame(frame);
	});
</script>

<div class="pointer-events-none absolute top-0 left-0 h-full w-full">
	<div class="relative h-full w-full overflow-hidden">
		{#each confetti as c}
			<span class="absolute text-2xl" style="left: {c.x}%; top: {c.y}%; transform: scale({c.r})"
				>{c.character}</span
			>
		{/each}
	</div>
</div>
<div
	class="flex h-full flex-col items-center justify-center gap-y-32 text-6xl text-lemon md:text-8xl"
>
	{#if winner}
		<h1>You win 🥳🎉</h1>
	{:else}
		<h1>You lose 😭</h1>
		<p class="text-4xl">
			{$game[$enemyGameId].nickname}'s character was:
			<span class="text-ua">{prettifyCharacterName($gameEndInfo.character_name)}</span>
		</p>
	{/if}
	{#if $game[$myGameId].creator}
		<Button
			disabled={time === 0}
			onClickFunc={(e) => {
				sendTask(e, 'restart_game');
			}}>Play Again</Button
		>
	{:else}
		<TextLoading style="text-2xl">Wating for the creator to restart the game</TextLoading>
	{/if}
</div>
