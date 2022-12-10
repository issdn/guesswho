<script>
	import { onDestroy } from 'svelte';
	import { notifications } from '../../stores';
	import Notification from './Notification.svelte';

	onDestroy(() => {
		notifications.set([]);
	});
</script>

<div
	class="pointer-events-none fixed inset-x-0 inset-y-0 flex flex-col items-center justify-start font-['Roboto_Mono']"
>
	{#each $notifications as notification (notification.id)}
		<Notification index={notification.id} visible={true} message={notification.message} />
	{/each}
</div>
