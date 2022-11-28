<script lang="ts">
import {
    sendTask
} from "../socketStore";
import {
    token,
    pickedCharacter,
    baseUrl,
    guessing
} from "../stores";
import {
    shadowhandler,
    conditionalhandler
} from "../actions"

export let darken: (value: boolean) => void;
export let characterName: string;

const prettyCharacterName: string = characterName.split("_").join(" ")

let isFlipped: boolean = false
$: isGuessing = $guessing && $pickedCharacter !== ""
$: isPicking = $pickedCharacter === ""

const fetchImage = (async () => {
    const response = await fetch(`${$baseUrl}/${$token}/characters/${characterName}`)
    return await response
})()

const flip = (e: Event) => {
    isFlipped = !isFlipped
}

const handleGuessCharacter = (e: Event) => {
    sendTask(e, "guess_character", {
        character_name: characterName
    });
    darken(false);
}

const handlePickCharacter = (e: Event) => {
    sendTask(e, "pick_starting_character", {
        character_name: characterName
    });
    darken(false);
}

const getCurrentAction = (isPicking: boolean, isGuessing: boolean) => {
    if (isGuessing) return handleGuessCharacter
    else if (isPicking) return handlePickCharacter
    else return flip
}

$: currentAction = getCurrentAction(isPicking, isGuessing)
</script>

<div
    use:conditionalhandler={currentAction}
    use:shadowhandler={isGuessing||isPicking}
    on:shadowenter={() => {darken(true)}}
    on:shadowleave={() => {darken(false)}}
    class="min-w-[8rem] sm:w-40 min-h-[11.5rem] sm:min-h-[13.5rem] hover:z-10 p-2 rounded-xl preserve3d bg-lemon duration-500 cursor-pointer border-4 border-[#FFA90A]
    {isFlipped ? 'flip-y' : ''}
    {isGuessing||isPicking ? 'hover:-translate-y-3' : ''}"
    >
    {#await fetchImage}
    <p>loading...</p>
    {:then data}
    <div class="w-full h-full transition-transform duration-1000 preserve3d">
        <div class="absolute bg-lemon backface-hidden rotate-y-0">
            <img src={data.url} alt="character" class="border-2 border-[#FFA90A]">
            <p class="text-lg sm:text-xl text-center my-[.15rem]">{prettyCharacterName}</p>
        </div>
        <div class="absolute h-full w-full backface-hidden bg-lemon flip-y">
            <div class="relative h-full w-full">
                <p class="absolute left-[50%] top-[50%] -translate-y-1/2 -translate-x-1/2 rotate-12 text-[10rem] opacity-10">?</p>
                <p class="absolute left-[50%] top-[50%] -translate-y-1/2 -translate-x-1/2 text-3xl text-center">{prettyCharacterName}</p>
            </div>
        </div>
    </div>

    {/await}
</div>
