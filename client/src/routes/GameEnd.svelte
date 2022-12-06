<script lang="ts">
import {
    sendTask
} from "../socketStore";
import {
    onMount
} from "svelte";
import {
    gameEndInfo,
    myGameId,
    enemyGameId,
    game
} from "../stores"
import Button from "./Button.svelte";
import { prettifyCharacterName } from "../scripts";

let time = 3;
onMount(() => {
    setInterval(() => {
        if (time = 0) return;
        else time--;
    }, 1000);
})
</script>

<div class="flex flex-col h-full gap-y-32 items-center justify-center text-8xl text-lemon">
    {#if $gameEndInfo.winner_id === $myGameId}
    <h1>You win 🥳🎉</h1>
    {:else}
    <h1>You lose 😭</h1>
    <p class="text-4xl">{$game[$enemyGameId].nickname}'s character was: <span class="text-ua">{prettifyCharacterName($gameEndInfo.character_name)}</span></p>
    {/if}
    {#if $game[$myGameId].creator}
    <Button disabled={time === 0} onClickFunc={(e)=>{sendTask(e ,"restart_game")}}>Play Again</Button>
    {/if}
</div>
