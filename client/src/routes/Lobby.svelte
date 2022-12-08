<script lang="ts">
	import { game, myGameId, enemyGameId, token, sendToast } from '../stores';
	import Button from './Button.svelte';
	import { sendTask } from '../socketStore';

	$: canStart = $game[$myGameId].ready && $game[$enemyGameId].ready;
</script>

<div class="w-full h-full flex flex-col py-16 gap-y-16 items-center text-lemon">
	<div class="text-4xl flex flex-row gap-x-2 items-center">
		<p>your token 🤐:</p>
		<p
			on:keydown={null}
			on:click={() => {
				navigator.clipboard.writeText($token).then(() => {
					sendToast('Copied!', 2000, 'success');
				});
			}}
			class="bg-space px-2 py-1 rounded-xl cursor-pointer"
		>
			{$token}
		</p>
	</div>
	<div class="flex flex-col h-full justify-around items-center">
		<div class="flex flex-row gap-x-16 text-6xl items-center">
			<div>
				<p>{$game[$myGameId].nickname}</p>
				<p class="text-xl text-right">(you)</p>
			</div>
			{#each Object.entries($game) as [id, player]}
				{#if parseInt(id) !== $myGameId}
					<p class="text-9xl rotate-12">VS</p>
					<div class="flex flex-col">
						<p>{player.nickname}</p>
						<p class="text-xl">{player.ready ? 'ready' : 'not ready'}</p>
					</div>
				{/if}
			{/each}
		</div>
		<div class="w-96 flex flex-col gap-y-4">
			<Button onClickFunc={(e) => sendTask(e, 'player_ready')} disabled={!$game[$enemyGameId]}>
				{$game[$myGameId].ready ? 'ready' : 'not ready'}
			</Button>
			{#if $game[$myGameId].creator}
				<Button onClickFunc={(e) => sendTask(e, 'start_game')} disabled={!canStart}>Start</Button>
			{/if}
		</div>
	</div>
</div>
