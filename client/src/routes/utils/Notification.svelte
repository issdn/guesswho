<script lang="ts">
	import { removeNotification } from '../../stores';
	import { slide } from 'svelte/transition';
	import { randomEmoji } from '../../scripts';
	import CloseButton from './CloseButton.svelte';

	const sleep = (time: number) => new Promise((res) => setTimeout(res, time));

	export let index: string;
	export let visible: boolean = false;
	export let message: string;

	const close = () => {
		visible = false;
		sleep(1000).then(() => removeNotification(index));
	};
</script>

{#if visible}
	<div
		transition:slide
		class="text-black-500 pointer-events-auto mt-4 rounded-xl bg-lemon font-['Mouse_Memoirs'] drop-shadow-xl md:w-96"
	>
		<div class="flex items-center justify-center rounded-xl py-2 px-6 text-center text-2xl">
			<p>{randomEmoji()}</p>
			<p class="w-full">{message}</p>
			<div class="flex items-center justify-end text-4xl">
				<div
					on:click={close}
					on:keydown={close}
					on:keypress={close}
					class="ml-2 h-fit w-fit cursor-pointer rounded-md px-2"
				>
					<CloseButton onClickFunc={close} style={'hover:bg-lemonh'} />
				</div>
			</div>
		</div>
	</div>
{/if}
