<script lang="ts">
import {
    onMount
} from "svelte";
import Character from "./Character.svelte";
import { fade } from 'svelte/transition';
import {token} from "./stores"

let darkened: boolean = false
const darken = (value: boolean) => darkened = value

let imageNames: [string];

onMount( async () => {
    await fetch(`http://127.0.0.1:8000/${$token}/characters`)
        .then((response) => response.json())
            .then((data) => imageNames = data.names)
    console.log(imageNames)
})
</script>

{#if imageNames}
<div class="w-full h-full sm:px-12 md:px-24 pt-8 flex flex-col gap-16">
    <div class="bg-secondaryYellow w-48 h-32 rounded-xl">10:20</div>
    <div class="w-full h-full flex flex-row gap-2 flex-wrap justify-center rounded-xl">
        {#each imageNames as name}
        <Character characterName={name} darken={darken}/>
        {/each}
    </div>
    {#if darkened}
        <div transition:fade={{delay: 200}} class="fixed top-0 left-0 w-screen h-screen bg-black opacity-75 pointer-events-none transition-transform duration-1000"/>
    {/if}
</div>
{/if}