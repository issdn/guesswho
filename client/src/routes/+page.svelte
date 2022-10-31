<script lang="ts">
    import Lobby from "./Lobby.svelte"
	import { handleTask } from "./socket";
    import { token, player } from "./stores"

    let inLobby = false;

    let ws: WebSocket;

    const joinLobby = async () => {
        ws = new WebSocket(`ws://localhost:8000/${$token}/lobby/ws`);
        ws.onopen = (event: Event) => {
            ws.send(JSON.stringify({type: "task", "task": "player_join", nickname: $player.nickname}))
        }
        ws.onmessage = (event: MessageEvent)=>{
            const message = JSON.parse(JSON.parse(event.data));
            console.log(message)
            if(message.type === "error") {
                alert(message.message)
                return;
            } else {
                handleTask(message)
                inLobby = true;
                return;
            }
        }
    }

    const createNewGame = async () => {
        await fetch("http://127.0.0.1:8000/newgame", {method: "POST"}).
            then((response) => response.json()).
                then((data)=>{
                    if (data.type == "info") {
                        token.set(data.token)
                        joinLobby()
                    }
                });
    }
</script>


<div class="py-24 flex flex-col w-full items-center gap-y-16">
    <div class="text-secondaryYellow">
        <h1 class="text-9xl">Guess Who?</h1>
        <p class="text-2xl float-right -rotate-6">The Game</p>
    </div>
    <div class="text-2xl flex flex-col gap-y-8">
        {#if !inLobby}
            <div>
                <input bind:value={$player.nickname}/>
            </div>
            <button on:click={createNewGame} class="flex flex-row gap-x-4 bg-secondaryYellow text-black-600 px-8 py-2 rounded-full">
                <p class="w-full text-center">
                    Create a Game
                </p>
            </button>      
            <div class="flex flex-row gap-x-8 bg-secondaryYellow px-8 py-2 rounded-full">
                <input bind:value={$token} class="bg-transparent h-full border-black"/>
                <span class="border-black border-r-2"/>
                <button class="text-black" on:click={joinLobby}>
                    Join 
                </button>
            </div>      
        {:else}
            <Lobby ws={ws}/>
        {/if}
    </div>
</div>
