<script lang="ts">
    import Lobby from "./Lobby.svelte"
    import { token, nickname } from "./stores"

    let gameCreated = false;

    const createNewGame = async () => {
        await fetch("http://127.0.0.1:8000/newgame", {method: "POST"}).
            then((response) => response.json()).
                then((data)=>{
                    token.set(data.init.token)
                    gameCreated = true;
                });
    }
</script>


<div class="py-24 flex flex-col w-full items-center gap-y-16">
    <div class="text-secondaryYellow">
        <h1 class="text-9xl">Guess Who?</h1>
        <p class="text-2xl float-right -rotate-6">The Game</p>
    </div>
    <div class="text-2xl flex flex-col gap-y-8">
        {#if !gameCreated}
            <div>
                <input bind:value={$nickname}/>
            </div>
            <button on:click={createNewGame} class="flex flex-row gap-x-4 bg-secondaryYellow text-black-600 px-8 py-2 rounded-full">
                <p class="w-full text-center">
                    Create a Game
                </p>
            </button>      
            <div class="flex flex-row gap-x-8 bg-secondaryYellow px-8 py-2 rounded-full">
                <input class="bg-transparent h-full border-black"/>
                <span class="border-black border-r-2"/>
                <button class="text-black">
                    Join 
                </button>
            </div>      
        {:else}
            <Lobby/>
        {/if}
    </div>
</div>
