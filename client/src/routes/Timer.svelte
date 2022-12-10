<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Config } from '../config';
	import { timer, gamePhase } from '../stores';

	$: if ($gamePhase === 'ask') timer.setNew(Config.ASKING_TIME);
	else if ($gamePhase === 'answer') timer.setNew(Config.ANSWERING_TIME);
	else if ($gamePhase === 'pick') timer.setNew(Config.PICKING_TIME);

	const interval = setInterval(() => {
		if ($timer > 0) timer.decrement();
	}, 1000);

	onDestroy(() => {
		clearInterval(interval);
	});
</script>

<p class="w-16 text-7xl {$timer > 10 ? 'text-lemon' : 'text-ua'}">
	{$timer}
</p>
