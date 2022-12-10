<script lang="ts">
	import { sendTask } from '../../socketStore';
	import { token, picking, canGuess, pickedCharacter } from '../../stores';
	import { shadowhandler, conditionalhandler } from '../../actions';
	import { Config } from '../../config';
	import { prettifyCharacterName } from '../../scripts';
	import Spinner from '../utils/Spinner.svelte';

	export let darken: (value: boolean) => void;
	export let characterName: string;
	export let imageFileName: string;

	const prettyCharacterName: string = prettifyCharacterName(characterName);

	let isFlipped: boolean = false;

	const fetchImage = (async () => {
		const response = await fetch(`${Config.BASE_URL}/${$token}/characters/${imageFileName}`);
		return await response;
	})();

	const flip = (e: Event) => {
		isFlipped = !isFlipped;
	};

	const handleGuessCharacter = (e: Event) => {
		sendTask(e, 'guess_character', {
			character_name: characterName
		});
		darken(false);
	};

	const handlePickCharacter = (e: Event) => {
		sendTask(e, 'pick_starting_character', {
			character_name: characterName
		});
		darken(false);
	};

	let currentAction: (e: Event) => void;
	$: if ($picking) currentAction = handlePickCharacter;
	else if ($canGuess) currentAction = handleGuessCharacter;
	else currentAction = flip;
</script>

<div
	use:conditionalhandler={currentAction}
	use:shadowhandler={$canGuess || $picking}
	on:shadowenter={() => {
		darken(true);
	}}
	on:shadowleave={() => {
		darken(false);
	}}
	class="min-h-[11.5rem] min-w-[8rem] cursor-pointer rounded-xl border-4 border-[#FFA90A] bg-lemon p-2 duration-500 preserve3d hover:z-10 sm:min-h-[13.5rem] sm:w-40
	{characterName === $pickedCharacter
		? "after:absolute after:-top-1 after:right-4 after:h-8 after:w-4 after:bg-ua after:content-[''] after:clip-path"
		: ''}
    {isFlipped ? 'flip-y' : ''}
    {$canGuess || $picking ? 'hover:-translate-y-3' : ''}"
>
	{#await fetchImage}
		<Spinner />
	{:then data}
		<div class="w-full h-full transition-transform duration-1000 preserve3d">
			<div class="absolute bg-lemon backface-hidden rotate-y-0">
				<img src={data.url} alt="character" class="border-2 border-[#FFA90A]" />
				<p class="text-lg sm:text-xl text-center my-[.15rem]">
					{prettyCharacterName}
				</p>
			</div>
			<div class="absolute h-full w-full backface-hidden bg-lemon flip-y">
				<div class="relative h-full w-full">
					<p
						class="absolute left-[50%] top-[50%] -translate-y-1/2 -translate-x-1/2 rotate-12 text-[10rem] opacity-10"
					>
						?
					</p>
					<p
						class="absolute left-[50%] top-[50%] -translate-y-1/2 -translate-x-1/2 text-3xl text-center"
					>
						{prettyCharacterName}
					</p>
				</div>
			</div>
		</div>
	{/await}
</div>
