<script lang="ts">
import {
    onMount
} from "svelte"
import {
    handleTask
} from "./socket";
import {
    lobby,
    my_lobby_id
} from "./stores"

export let ws: WebSocket;

const sendTask = (event: Event, taskType: string) => {
    ws.send(JSON.stringify({
        task: taskType,
        lobby_id: $my_lobby_id
    }))
    event.preventDefault();
}

onMount(() => {
    ws.onmessage = (event: MessageEvent < string > ) => {
        const message = JSON.parse(JSON.parse(event.data));
        handleTask(message)
    }
})
</script>

<div class="flex flex-col gap-y-8 justify-center items-center text-secondaryYellow">
    <p class="text-4xl">you: {$lobby[$my_lobby_id].nickname}</p>
    {#each Object.entries($lobby) as [id, player] }
    {#if parseInt(id) !== $my_lobby_id}
    <div class="flex flex-row gap-x-1">
        <p class="text-4xl">enemy: {player.nickname}</p>
        {#if parseInt(id) !== $my_lobby_id}
        <p class="text-lg">{player.ready ? "ready" : "not ready"}</p>
        {/if}
    </div>
    {/if}
    {/each}
    <button on:click={(e) => sendTask(e, "player_ready")} class="uppercase bg-secondaryYellow rounded-md px-16 text-2xl text-black">{$lobby[$my_lobby_id].ready ? "ready" : "not ready"}</button>
</div>
