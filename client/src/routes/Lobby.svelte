<script lang="ts">
	import { onMount } from "svelte";
    import { token, nickname } from "./stores"


    let ws: WebSocket;

    const sendTask = (event: Event, task: string) => {
        ws.send(JSON.stringify({type: "task", "task": task}))
        event.preventDefault()
    }

    onMount(()=>{
        ws = new WebSocket(`ws://localhost:8000/${$token}/lobby/ws`);
        ws.onopen = (event: Event) => {
            ws.send(JSON.stringify({type: "init", nickname: $nickname}))
        }
        ws.onmessage = (event: MessageEvent)=>{
            const message = JSON.parse(JSON.parse(event.data));
            console.log(message)
        }
    })
</script>

<div class="flex flex-col justify-center items-center">
    <button on:click={(e) => sendTask(e, "player_ready")} class="uppercase bg-secondaryYellow rounded-md px-16 text-2xl">ready</button>
</div>