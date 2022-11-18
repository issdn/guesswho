<script lang="ts">
	import CharacterInside from "./CharacterInside.svelte";
import {
    sendTask
} from "./socketStore";
import {
    token,
    pickedCharacter
} from "./stores";

export let darken: (value: boolean) => void;
export let characterName: string;
const prettyCharacterName: string = characterName.split("_").join(" ")

let isFlipped: boolean = false

const fetchImage = (async () => {
    const response = await fetch(`http://127.0.0.1:8000/${$token}/characters/${characterName}`)
    return await response
})()
</script>

<div class="min-w-[8rem] sm:w-32 min-h-[12rem] hover:z-10">
    {#await fetchImage}
    <p>loading...</p>
    {:then data}
    {#if !$pickedCharacter}
    <div
        on:mouseenter={() => {darken(true)}}
        on:mouseleave={() => {darken(false)}} 
        on:keydown={()=>{}}
        on:click={(e)=>{sendTask(e, "pick_starting_character", {
            character_name: characterName}); 
            darken(false);
        }}
        class="w-full h-full p-2 rounded-xl preserve3d bg-secondaryYellow duration-500 cursor-pointer border-2 border-black hover:-translate-y-3"
    >
        <CharacterInside characterName={prettyCharacterName} url={data.url}/>
    </div>
    {:else}
    <div 
        on:keydown={()=>{}}
        on:click={() => {isFlipped = !isFlipped}}
        class="w-full h-full p-2 rounded-xl preserve3d bg-secondaryYellow duration-500 cursor-pointer border-2 border-black {isFlipped ? 'rotate-y' : ''}"
    >
        <CharacterInside characterName={prettyCharacterName} url={data.url}/>
    </div>
    {/if}
    {/await}
</div>
