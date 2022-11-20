<script lang="ts">
import {
    onMount
} from "svelte";
import Character from "./Character.svelte";
import {
    fade
} from 'svelte/transition';
import {
    token,
    baseUrl,
    myGameId,
    asking,
    question
} from "./stores"
import Modal from "./Modal.svelte";
import {
    sendTask
} from "./socketStore";

let isAskModalOpen = false
const setAskModalOpen = () => {
    isAskModalOpen = true
}
const setAskModalClose = () => {
    isAskModalOpen = false
}

let isAnswerModalOpen = false
const setAnswerModalOpen = () => {
    isAnswerModalOpen = true
}
const setAnswerModalClose = () => {
    isAnswerModalOpen = false
}

/* Darken the screen when choosing a character. */
let darkened: boolean = false
const darken = (value: boolean) => darkened = value

let imageNames: [string];

let newQuestion: string;

onMount(async () => {
    await fetch(`${$baseUrl}/${$token}/characters`)
        .then((response) => response.json())
        .then((data) => imageNames = data.names)

    fetch(`${$baseUrl}/${$token}/starting_player`)
        .then(res => res.json())
        .then(data => (parseInt(data.starting_player_id)) === $myGameId ? asking.set(true) : asking.set(false))
})
</script>

<Modal modalOpen={isAskModalOpen} closeModal={setAskModalClose}>
    <h1 class="text-black text-4xl text-center">Ask a question</h1>
    <textarea bind:value={newQuestion} class="h-full resize-none p-2 text-xl rounded-xl"/>
        <div class="w-full flex flex-row justify-between">
            <button on:click={(e) => {sendTask(e, "ask_question", {question: newQuestion})}} class="px-8 py-1 bg-primaryRed rounded-xl">Ask</button>
            <button on:click={setAskModalClose} class="px-8 py-1 border-2 border-primaryRed rounded-xl text-primaryRed">Cancel</button>
        </div>
        </Modal>

        <Modal modalOpen={isAnswerModalOpen} closeModal={setAnswerModalClose}>
            <h1 class="text-black text-4xl text-center">Answer!</h1>
            <textarea class="h-full resize-none p-2 text-xl rounded-xl"/>
                </Modal>

                {#if imageNames}
                <div class="w-full h-full sm:px-12 md:px-24 pt-8 flex flex-col gap-16">
                    <div class="w-full h-32 flex flex-row">
                        <div class="bg-secondaryYellow w-48 h-full rounded-xl">10:20</div>
                        <div class="flex flex-col gap-2">
                            {#if $asking}
                            <button on:click={setAskModalOpen} class="bg-secondaryYellow h-fit px-4 py-1 rounded-md">Ask a question</button>
                            {:else}
                            <button on:click={setAnswerModalOpen} class="bg-secondaryYellow h-fit px-4 py-1 rounded-md">Answer the question</button>
                            {/if}
                        </div>
                        <p>{$question}</p>
                    </div>
                    <div class="w-full h-full flex flex-row gap-2 flex-wrap justify-center rounded-xl">
                        {#each imageNames as name}
                        <Character characterName={name} darken={darken}/>
                            {/each}
                            </div>
                            {#if darkened}
                            <div transition:fade={{delay: 200}} class="fixed top-0 left-0 w-screen h-screen bg-black opacity-75 pointer-events-none transition-transform duration-1000"/>
                                {/if}
                            </div>
                            {/if}
