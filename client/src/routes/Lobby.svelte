<script lang="ts">
import {
    onMount
} from "svelte"
	import { handleTask } from "./socket";
import {
    player,
    enemy
} from "./stores"

export let ws: WebSocket;

const sendTask = (event: Event, taskType: string) => {
    ws.send(JSON.stringify({
        type: "task",
        "task": taskType,
        lobby_id: $player.lobby_id
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

<div class="flex flex-col gap-y-8 justify-center items-center">
    <p class="text-4xl text-secondaryYellow">p1: {$player.nickname}</p>
    {#if $enemy.lobby_id != -1}
    <div class="flex flex-row gap-x-8 text-secondaryYellow">
        <p class="text-4xl">p2: {$enemy.nickname}</p>
        <p class="text-lg">{$enemy.ready ? "ready" : "not ready"}</p>
    </div>
    {/if}
    <button on:click={(e) => sendTask(e, "player_ready")} class="uppercase bg-secondaryYellow rounded-md px-16 text-2xl">{$player.ready ? "ready" : "not ready"}</button>
</div>
