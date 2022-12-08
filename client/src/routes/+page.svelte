<script lang="ts">
	import Game from './game/Game.svelte';
	import Lobby from './Lobby.svelte';
	import { token, phase, nickname } from '../stores';
	import { joinSocket } from '../socketStore';
	import ToastContainer from './utils/ToastContainer.svelte';
	import { Config } from '../config';
	import GameEnd from './GameEnd.svelte';

	const createNewGame = async () => {
		await fetch(`${Config.BASE_URL}/newgame`, { method: 'POST' })
			.then((response) => response.json())
			.then((data) => {
				if (data.task == 'init') {
					token.set(data.token);
				}
			});
		joinSocket();
	};
</script>

{#if $phase === ''}
	<div class="flex w-full flex-col items-center gap-y-16 py-24 md:px-[15%] xl:px-[33%]">
		<div class="text-lemon">
			<h1 class="text-9xl">Guess Who?</h1>
			<p class="float-right -rotate-6 text-2xl">The Game</p>
		</div>
		<div class="flex w-full flex-col gap-y-8 text-2xl">
			<div class="flex flex-row rounded-full border-2 border-lemon">
				<p class="-ml-1 h-[full] rounded-l-full bg-lemon px-4 py-2">name:</p>
				<div class="h-full w-full py-2 pl-4 pr-8">
					<input
						class="w-full border-b-2 border-lemon bg-transparent text-lemon focus:outline-none"
						bind:value={$nickname}
					/>
				</div>
			</div>
			<button
				on:click={createNewGame}
				class="flex flex-row gap-x-4 rounded-full bg-lemon px-8 py-2 text-black hover:bg-lemonh"
			>
				<p class="w-full text-center">Create a Game</p>
			</button>
			<div class="flex flex-row rounded-full border-2 border-lemon">
				<div class="h-full w-full py-2 pl-8 pr-4">
					<input
						class="w-full border-b-2 border-lemon bg-transparent text-lemon focus:outline-none"
						bind:value={$token}
					/>
				</div>
				<button
					class="-ml-1 h-[full] rounded-r-full bg-lemon px-12 py-2 hover:bg-lemonh"
					on:click={joinSocket}
				>
					Join
				</button>
			</div>
		</div>
	</div>
{:else if $phase === 'lobby'}
	<Lobby />
{:else if $phase === 'game'}
	<Game />
{:else if $phase === 'end'}
	<GameEnd />
{/if}
<ToastContainer />
