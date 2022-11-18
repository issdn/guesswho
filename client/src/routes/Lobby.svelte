<script lang="ts">
import {
    game,
    myGameId,
    enemyGameId,
    token
} from "./stores"

import {sendTask} from "./socketStore"

$: canStart = $game[$myGameId].ready && $game[$enemyGameId].ready

</script>

<div class="flex flex-col gap-y-8 justify-center items-center text-secondaryYellow">
    <p>your token 🤐: {$token}</p>
    <p class="text-4xl">you: {$game[$myGameId].nickname}</p>
    {#each Object.entries($game) as [id, player] }
    {#if parseInt(id) !== $myGameId}
    <div class="flex flex-row gap-x-1">
        <p class="text-4xl">enemy: {player.nickname}</p>
        <p class="text-lg">{player.ready ? "ready" : "not ready"}</p>
    </div>
    {/if}
    {/each}
    <button disabled={!$game[$enemyGameId]} on:click={(e) => {sendTask(e, "player_ready");}}
        class="uppercase bg-secondaryYellow rounded-md px-16 text-2xl text-black {!$game[$enemyGameId] ? 'cursor-not-allowed' : ''}">
        {$game[$myGameId].ready ? "ready" : "not ready"}
    </button>
    {#if $game[$myGameId].creator}
    <button on:click={(e) => sendTask(e, "start_game")} disabled={!canStart}
        class="uppercase bg-secondaryYellow rounded-md px-16 text-2xl text-black {!canStart ? 'cursor-not-allowed' : ''}">
        start!
    </button>
    {/if}
</div>
