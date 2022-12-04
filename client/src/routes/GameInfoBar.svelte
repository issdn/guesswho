<script lang="ts">
    import Modal from "./Modal.svelte"
    import {asking, question, game, enemyGameId, pickedCharacter, guessing} from "../stores"
    import {sendTask} from "../socketStore"
    import Button from "./Button.svelte";
	import Spinner from "./Spinner.svelte"; 	import TextLoading from "./TextLoading.svelte";
	import Timer from "./Timer.svelte";

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
<div class="w-full flex flex-col xl:flex-row gap-x-24 border-2 border-lemon items-center py-4 px-8 xl:px-24 gap-y-4 rounded-xl">
    <Timer time={60}/>
    <div class="flex flex-row w-full gap-x-24 gap-y-4 xl:gap-y-0 items-center justify-center xl:justify-between flex-wrap text-lemon text-4xl "> 
        {#if !$pickedCharacter}
        <TextLoading>It's your time to pick a character</TextLoading>
        {:else}
        {#if $asking}
            {#if !asked}
                {#if $pickedCharacter}
                <div class="flex flex-col items-center gap-y-4 md:flex-row md:gap-x-8">
                    <Button onClickFunc={setAskModalOpen}>
                        Ask a question
                    </Button>
                    <div class="text-lemon text-4xl">or</div>
                    <Button onClickFunc={() => guessing.set(!$guessing)} style={$guessing ? "bg-lemonh" : "bg-lemon"}>
                        {#if !$guessing}
                            guess the character
                        {:else}
                        <TextLoading>
                            guessing
                        </TextLoading>
                        {/if}
                    </Button>
                </div>
                {:else}
                <TextLoading>It's your time to pick a character</TextLoading>
                {/if}
            {:else}
            <TextLoading>{$game[$enemyGameId].nickname}&nbsp;is answering</TextLoading>
            {/if}
        {:else}
            {#if $question}
            <p>{$game[$enemyGameId].nickname}:&nbsp;{$question}</p>
            <div class="flex flex-row gap-2 text-black">
                <button on:click={(e) => {handleQuestionAnswer(e, "yes")}} class="bg-lemon px-4 py-1 h-fit rounded-md hover:bg-mikado">Yes!</button>
                <button on:click={(e) => {handleQuestionAnswer(e, "no")}} class="bg-lemon px-4 py-1 h-fit rounded-md hover:bg-mikado">No!</button>
                <button on:click={(e) => {handleQuestionAnswer(e, "idk")}} class="bg-lemon px-4 py-1 h-fit rounded-md hover:bg-mikado">I don't understand.</button>
            </div>
            {:else}
            <TextLoading>{$game[$enemyGameId].nickname}&nbsp;is asking</TextLoading>
            {/if}
        {/if}
        {/if}
    </div>
</div>

<Modal modalOpen={isAskModalOpen} closeModal={setAskModalClose}>
    <h1 class="text-black text-4xl text-center">Ask a question!</h1>
    <textarea bind:value={newQuestion} class="h-full resize-none p-2 text-xl rounded-xl"/>
        <div class="w-full flex flex-row justify-between">
            <button on:click={(e) => {handleQuestionSend(e)}} class="px-8 py-1 bg-space rounded-xl">Ask</button>
            <button on:click={setAskModalClose} class="px-8 py-1 border-2 border-space rounded-xl text-space">Cancel</button>
        </div>
        </Modal>