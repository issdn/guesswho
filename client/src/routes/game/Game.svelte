<script lang="ts">
	import { onMount } from 'svelte';
	import Character from './Character.svelte';
	import { fade } from 'svelte/transition';
	import { token } from '../../stores';
	import GameInfoBar from './GameInfoBar.svelte';
	import { Config } from '../../config';

	/* Darken the screen when choosing a character. */
	let darkened: boolean = false;
	const darken = (value: boolean) => (darkened = value);

	let imageNames: [string, string][];

	onMount(async () => {
		await fetch(`${Config.BASE_URL}/${$token}/characters`)
			.then((response) => response.json())
			.then((data) => (imageNames = data));
	});
</script>

{#if imageNames}
	<div class="flex h-full w-full flex-col gap-16 pt-8 sm:px-12 md:px-24">
		<GameInfoBar />
		<div class="flex h-full w-full flex-row flex-wrap justify-center gap-2 rounded-xl">
			{#each imageNames as imageTuple}
				<Character characterName={imageTuple[0]} imageFileName={imageTuple[1]} {darken} />
			{/each}
		</div>
		{#if darkened}
			<div
				transition:fade={{ delay: 200 }}
				class="pointer-events-none fixed top-0 left-0 h-screen w-screen bg-black opacity-75 transition-transform duration-1000"
			/>
		{/if}
	</div>
{/if}
