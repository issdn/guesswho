<script lang="ts">
	import { slide } from 'svelte/transition';
	import { sendTask } from '../../socketStore';

	export let setModalClose: () => void;

	let newQuestion: string = '';
	let error: string = '';

	$: newQuestion.length > 64 ? (error = 'Question too long!') : (error = '');

	const handleQuestionSend = (e: Event) => {
		sendTask(e, 'ask_question', {
			question: newQuestion
		});
		newQuestion = '';
		setModalClose();
	};
</script>

<h1 class="text- text-center text-4xl">Ask a question!</h1>
<div class="flex h-1/2 flex-col gap-y-2">
	<textarea
		bind:value={newQuestion}
		class="resize-none rounded-xl p-2 text-xl outline-none outline-offset-0 {error
			? 'focus:outline-ua'
			: 'focus:outline-cornflowerh'}"
	/>
	{#if error}
		<div class="relative w-full">
			<div transition:slide class="absolute w-full rounded-md bg-ua px-4 text-lg">
				<p class="text-white">{error}</p>
			</div>
		</div>
	{/if}
</div>
<div class="flex w-full flex-col justify-between gap-y-2">
	<button
		disabled={error !== ''}
		on:click={(e) => {
			handleQuestionSend(e);
		}}
		class="rounded-2xl bg-cornflower px-8 py-1 text-xl text-white {error
			? 'cursor-not-allowed'
			: 'hover:bg-cornflowerh'}">Ask</button
	>
	<button
		on:click={setModalClose}
		class="hover:cornflowerh rounded-2xl border-2 border-cornflower px-8 py-1 text-xl text-cornflower hover:text-cornflowerh"
		>Cancel</button
	>
</div>
