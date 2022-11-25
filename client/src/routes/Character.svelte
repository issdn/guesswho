<script lang="ts">
	import CharacterInside from "./CharacterInside.svelte";
import {
    sendTask
} from "./socketStore";
import {
    token,
    pickedCharacter,
    baseUrl,
    guessing
} from "./stores";
import {shadowhandler, conditionalhandler} from "./actions"


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

const flip = (e: Event) => {isFlipped = !isFlipped}

const handleGuessCharacter = (e: Event) => {
    sendTask(e, "guess_character", {character_name: characterName}); 
    darken(false);
}

const handlePickCharacter = (e: Event) => {
    sendTask(e, "pick_starting_character", {character_name: characterName}); 
    darken(false);
}

const getCurrentAction = (isPicking: boolean, isGuessing: boolean) => {
    if(isGuessing) return handleGuessCharacter 
    else if (isPicking) return handlePickCharacter
    else return flip
}

$: currentAction = getCurrentAction(isPicking, isGuessing)

</script>

<div class="min-w-[8rem] sm:w-40 min-h-[11.5rem] sm:min-h-[13.5rem] hover:z-10">
    {#await fetchImage}
    <p>loading...</p>
    {:then data}
    <div
        use:conditionalhandler={currentAction}
        use:shadowhandler={isGuessing||isPicking}
        on:shadowenter={() => {darken(true)}}
        on:shadowleave={() => {darken(false)}}
        class="w-full h-full p-2 rounded-xl preserve3d bg-safety duration-500 cursor-pointer border-4 border-[#FF8900] 
        {isFlipped ? 'flip-y' : ''} 
        {isGuessing||isPicking ? 'hover:-translate-y-3' : ''}"
    >
        <CharacterInside characterName={prettyCharacterName} url={data.url}/>
    </div>
    {/await}
</div>
