<script lang="ts">
import {
    lobby,
    myLobbyId,
    enemyLobbyId,
    token
} from "./stores"

import {sendTask} from "./socketStore"

$: canStart = $lobby[$myLobbyId].ready && $lobby[$enemyLobbyId].ready

</script>

<div class="flex flex-col gap-y-8 justify-center items-center text-secondaryYellow">
    <p>your token 🤐: {$token}</p>
    <p class="text-4xl">you: {$lobby[$myLobbyId].nickname}</p>
    {#each Object.entries($lobby) as [id, player] }
    {#if parseInt(id) !== $myLobbyId}
    <div class="flex flex-row gap-x-1">
        <p class="text-4xl">enemy: {player.nickname}</p>
        <p class="text-lg">{player.ready ? "ready" : "not ready"}</p>
    </div>
    {/if}
    {/each}
    <button disabled={!$lobby[$enemyLobbyId]} on:click={(e) => {sendTask(e, "player_ready");}}
        class="uppercase bg-secondaryYellow rounded-md px-16 text-2xl text-black {!$lobby[$enemyLobbyId] ? 'cursor-not-allowed' : ''}">
        {$lobby[$myLobbyId].ready ? "ready" : "not ready"}
    </button>
    {#if $lobby[$myLobbyId].creator}
    <button on:click={(e) => sendTask(e, "start")} disabled={!canStart}
        class="uppercase bg-secondaryYellow rounded-md px-16 text-2xl text-black {!canStart ? 'cursor-not-allowed' : ''}">
        start!
    </button>
    {/if}
</div>
