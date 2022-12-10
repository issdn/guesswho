<script lang="ts">
	import Modal from '../Modal.svelte';
	import {
		asking,
		question,
		game,
		enemyGameId,
		pickedCharacter,
		guessing,
		gamePhase
	} from '../../stores';
	import { sendTask } from '../../socketStore';
	import Button from '../Button.svelte';
	import TextLoading from '../utils/TextLoading.svelte';
	import Timer from '../Timer.svelte';
	import AskQuestionModalInside from './AskQuestionModalInside.svelte';

	let isModalOpen = false;

	let enemyNickname = $game[$enemyGameId].nickname;

	const setModalOpen = () => {
		isModalOpen = true;
		console.log('DUMBASS');
	};
	const setModalClose = () => {
		isModalOpen = false;
	};

	const handleQuestionAnswer = (e: Event, answer: 'yes' | 'no' | 'idk') => {
		sendTask(e, 'answer_question', {
			answer: answer
		});
	};
</script>

<div
	class="flex w-full flex-col items-center gap-x-16 gap-y-4 rounded-xl border-2 border-lemon py-4 px-8 xl:flex-row xl:px-24"
>
	<Timer />
	<div
		class="flex w-full flex-row flex-wrap items-center justify-center gap-x-24 gap-y-4 text-4xl text-lemon xl:justify-between xl:gap-y-0 "
	>
		{#if $gamePhase === 'pick'}
			{#if !$pickedCharacter}
				<TextLoading>It's your time to pick a character</TextLoading>
			{:else}
				<TextLoading>{enemyNickname}&nbsp;is picking a character</TextLoading>
			{/if}
		{:else if $gamePhase === 'ask'}
			{#if $asking}
				<div class="flex flex-col items-center gap-y-4 md:flex-row md:gap-x-8">
					<Button onClickFunc={setModalOpen}>Ask a question</Button>
					<div class="text-4xl text-lemon">or</div>
					<Button
						onClickFunc={() => guessing.set(!$guessing)}
						style={$guessing ? 'bg-lemonh' : 'bg-lemon'}
					>
						{#if !$guessing}
							guess the character
						{:else}
							<TextLoading>guessing</TextLoading>
						{/if}
					</Button>
				</div>
			{:else}
				<TextLoading>{enemyNickname}&nbsp;is asking</TextLoading>
			{/if}
		{:else if $gamePhase === 'answer'}
			{#if $question}
				<p class="break-all">{enemyNickname}:&nbsp;{$question}</p>
				<div class="flex flex-row gap-2 text-black">
					<button
						on:click={(e) => {
							handleQuestionAnswer(e, 'yes');
						}}
						class="hover:bg-mikado h-fit rounded-md bg-lemon px-4 py-1">Yes!</button
					>
					<button
						on:click={(e) => {
							handleQuestionAnswer(e, 'no');
						}}
						class="hover:bg-mikado h-fit rounded-md bg-lemon px-4 py-1">No!</button
					>
					<button
						on:click={(e) => {
							handleQuestionAnswer(e, 'idk');
						}}
						class="hover:bg-mikado h-fit rounded-md bg-lemon px-4 py-1">I don't understand.</button
					>
				</div>
			{:else}
				<TextLoading>{enemyNickname}&nbsp;is answering</TextLoading>
			{/if}
		{/if}
	</div>
</div>

<Modal modalOpen={isModalOpen} closeModal={setModalClose}>
	<AskQuestionModalInside {setModalClose} />
</Modal>
