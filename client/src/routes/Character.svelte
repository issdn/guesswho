<script lang="ts">
import {
    token
} from "./stores";

const randomRoundness = () => {
    return Math.floor(Math.random() * 45);
}

export let characterName: string;

const fetchImage = (async () => {
    const response = await fetch(`http://127.0.0.1:8000/${$token}/characters/${characterName}`)
    return await response
})()
</script>

<div class="w-full h-full bg-secondaryYellow p-2 rounded-md cursor-pointer hover:p-1">
    {#await fetchImage}
    <p>loading...</p>
    {:then data}
    <img src={data.url} alt="character">
    {/await}
</div>
