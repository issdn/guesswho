<script lang="ts">
	import { slide } from 'svelte/transition';
	import { removeToast } from '../../stores';
	import CloseButton from './CloseButton.svelte';
	const sleep = (time: number) => new Promise((res) => setTimeout(res, time));

	const types = {
		warning: 'bg-red-500',
		success: 'bg-green-500'
	};

	const btnTypes = {
		warning: 'hover:bg-red-400',
		success: 'hover:bg-green-400'
	};

	export let index: string;
	export let message = '';
	export let visible: boolean;
	export let type: 'warning' | 'success' = 'warning';

	const close = () => {
		visible = false;
		sleep(1000).then(() => removeToast(index));
	};
</script>

{#if visible}
	<div
		transition:slide
		class="pointer-events-auto mb-4 w-full px-4 font-['Mouse_Memoirs'] md:w-96 md:px-0"
	>
		<div
			class="{types[
				type
			]} flex items-center justify-center gap-x-4 rounded-xl px-4 py-2 text-center text-2xl text-white"
		>
			<p class="w-full">{message}</p>
			<div class="flex items-center justify-end text-4xl">
				<CloseButton onClickFunc={close} style={btnTypes[type]} />
			</div>
		</div>
	</div>
{/if}
