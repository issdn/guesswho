<script lang="ts">
import {
    onMount
} from "svelte";
	import Character from "./Character.svelte";
import {token} from "./stores"

let imageNames: [string];

onMount( async () => {
    await fetch(`http://127.0.0.1:8000/${$token}/characters`)
        .then((response) => response.json())
            .then((data) => imageNames = data.names)
    console.log(imageNames)
})
</script>

{#if imageNames}
    <div class="w-full px-24 pt-8">
        <div class="w-full grid gap-16 grid-cols-6 grid-rows-4">
            {#each imageNames as name}
            <Character characterName={name}/>
            {/each}
        </div>
    </div>
{/if}