<script lang="ts">
    import Modal from "./Modal.svelte"
    import {asking, question, answer, game, enemyGameId, pickedCharacter, guessing} from "./stores"
    import {sendTask} from "./socketStore"

    let newQuestion: string;
    let asked = false

    let isAskModalOpen = false
    
    const setAskModalOpen = () => {
        isAskModalOpen = true
    }
    const setAskModalClose = () => {
        isAskModalOpen = false
    }

    const handleQuestionSend = (e: Event) => {
        sendTask(e, "ask_question", {question: newQuestion})
        asked = true
        setAskModalClose()
    }

    const handleQuestionAnswer = (e: Event, answer: "yes" | "no" | "idk") => {
        sendTask(e, "answer_question", {answer: answer})
        question.set("")
        asked = false
    }

</script>
<div class="w-full flex flex-col xl:flex-row gap-x-24 border-2 border-safety items-center py-4 px-8 xl:px-24 gap-y-4 rounded-xl">
    <p class="text-7xl text-safety">0:59</p>
    <div class="flex flex-row w-full gap-x-24 gap-y-4 xl:gap-y-0 items-center justify-center xl:justify-between flex-wrap text-2xl"> 
        {#if $asking}
            {#if !asked}
                {#if $pickedCharacter}
                <div class="flex flex-row gap-x-8">
                    <button on:click={setAskModalOpen} class="bg-safety h-fit px-4 py-1 rounded-md">Ask a question</button>
                    <div class="text-safety text-4xl">or</div>
                    <button on:click={() => guessing.set(true)} class="bg-safety h-fit px-4 py-1 rounded-md">Guess the character</button>
                </div>
                {:else}
                <p class="text-safety text-4xl after:content-[''] after:animate-dots">It's your time to pick a character!</p>
                {/if}
            {:else}
            <p class="text-safety text-4xl after:content-[''] after:animate-dots">{$game[$enemyGameId].nickname}&nbsp;is answering</p>
            {/if}
        {:else}
            {#if $question}
            <p class="text-safety text-4xl after:content-[''] after:animate-dots">{$game[$enemyGameId].nickname}:&nbsp;{$question}</p>
            <div class="flex flex-row gap-2">
                <button on:click={(e) => {handleQuestionAnswer(e, "yes")}} class="bg-safety px-4 py-1 h-fit rounded-md hover:bg-mikado">Yes!</button>
                <button on:click={(e) => {handleQuestionAnswer(e, "no")}} class="bg-safety px-4 py-1 h-fit rounded-md hover:bg-mikado">No!</button>
                <button on:click={(e) => {handleQuestionAnswer(e, "idk")}} class="bg-safety px-4 py-1 h-fit rounded-md hover:bg-mikado">I don't understand.</button>
            </div>
            {:else}
                {#if $pickedCharacter}
                    <p class="text-safety text-4xl after:content-[''] after:animate-dots">{$game[$enemyGameId].nickname} is asking...</p>
                {:else}
                    <p class="text-safety text-4xl after:content-[''] after:animate-dots">It's your time to pick a character!</p>
                {/if}
            {/if}
        {/if}
    </div>
</div>

<Modal modalOpen={isAskModalOpen} closeModal={setAskModalClose}>
    <h1 class="text-black text-4xl text-center">Ask a question!</h1>
    <textarea bind:value={newQuestion} class="h-full resize-none p-2 text-xl rounded-xl"/>
        <div class="w-full flex flex-row justify-between">
            <button on:click={(e) => {handleQuestionSend(e)}} class="px-8 py-1 bg-salsa rounded-xl">Ask</button>
            <button on:click={setAskModalClose} class="px-8 py-1 border-2 border-salsa rounded-xl text-salsa">Cancel</button>
        </div>
        </Modal>