<script lang="ts">
	import { game, myGameId, enemyGameId, token, sendToast } from '../stores';
	import Button from './Button.svelte';
	import { sendTask } from '../socketStore';

	$: canStart = $game[$myGameId].ready && $game[$enemyGameId].ready;
</script>

<div class="flex h-full w-full flex-col items-center justify-between py-16 text-lemon md:gap-y-16">
	<div class="flex flex-col gap-y-2 gap-x-2 text-4xl md:flex-row md:items-center">
		<p>your token 🤐:</p>
		<p
			on:keydown={null}
			on:click={() => {
				navigator.clipboard.writeText($token).then(() => {
					sendToast('Copied!', 2000, 'success');
				});
			}}
			class="cursor-pointer rounded-xl bg-space px-2 py-1 text-center"
		>
			{$token}
		</p>
	</div>
	<div class="flex h-full flex-col items-center justify-around">
		<div
			class="flex flex-col items-center gap-y-4 text-4xl md:flex-row md:gap-y-0 md:gap-x-16 md:text-6xl"
		>
			<div>
				<p>{$game[$myGameId].nickname}</p>
				<p class="text-right text-xl">(you)</p>
			</div>
			{#each Object.entries($game) as [id, player]}
				{#if parseInt(id) !== $myGameId}
					<p class="rotate-12 text-7xl md:text-9xl">VS</p>
					<div class="flex flex-col">
						<p>{player.nickname}</p>
						<p class="text-xl">{player.ready ? 'ready' : 'not ready'}</p>
					</div>
				{/if}
			{/each}
		</div>
		<div class="flex w-96 flex-col gap-y-4 px-2">
			<Button onClickFunc={(e) => sendTask(e, 'player_ready')} disabled={!$game[$enemyGameId]}>
				{$game[$myGameId].ready ? 'ready' : 'not ready'}
			</Button>
			{#if $game[$myGameId].creator}
				<Button onClickFunc={(e) => sendTask(e, 'start_game')} disabled={!canStart}>Start</Button>
			{/if}
		</div>
	</div>
</div>
