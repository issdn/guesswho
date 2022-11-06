<script lang="ts">
    import Game from "./Game.svelte";
    import Lobby from "./Lobby.svelte"
    import { token, phase, nickname } from "./stores"
    import { joinSocket } from "./socketStore"

    const createNewGame = async () => {
        await fetch("http://127.0.0.1:8000/newgame", {method: "POST"}).
            then((response) => response.json()).
                then((data)=>{
                    if (data.task == "init") {
                        token.set(data.token)
                    }
                });
        joinSocket()
    }
</script>


{#if $phase === ""}
<div class="py-24 md:px-[15%] xl:px-[33%] flex flex-col w-full items-center gap-y-16">
    <div class="text-secondaryYellow">
        <h1 class="text-9xl">Guess Who?</h1>
        <p class="text-2xl float-right -rotate-6">The Game</p>
    </div>
    <div class="text-2xl flex flex-col gap-y-8 w-full">
            <div class="flex flex-row border-2 border-secondaryYellow rounded-full">
                <p class="h-[full] -ml-1 bg-secondaryYellow px-4 py-2 rounded-l-full">name: </p>
                <div class="h-full py-2 pl-4 pr-8 w-full">
                    <input class="w-full bg-transparent focus:outline-none text-secondaryYellow border-b border-secondaryYellow" bind:value={$nickname}/>
                </div>
            </div>
            <button on:click={createNewGame} class="flex flex-row gap-x-4 bg-secondaryYellow text-black px-8 py-2 rounded-full">
                <p class="w-full text-center">
                    Create a Game
                </p>
            </button>      
            <div class="flex flex-row border-2 border-secondaryYellow rounded-full">
                <div class="h-full py-2 pl-8 pr-4 w-full">
                    <input class="w-full bg-transparent focus:outline-none text-secondaryYellow border-b border-secondaryYellow" bind:value={$token}/>
                </div>
                <button class="h-[full] -ml-1 bg-secondaryYellow px-12 py-2 rounded-r-full" on:click={joinSocket}>
                    Join 
                </button>
            </div>      
        </div>
    </div>
{:else if $phase === "lobby"}
    <Lobby/>
{:else if $phase === "game"}
    <Game/>
{/if}
    