<script lang="ts">
import Modal from "../Modal.svelte"
import {
    asking,
    question,
    game,
    enemyGameId,
    pickedCharacter,
    guessing,
    gamePhase
} from "../../stores"
import {
    sendTask
} from "../../socketStore"
import Button from "../Button.svelte";
import TextLoading from "../utils/TextLoading.svelte";
import Timer from "../Timer.svelte";

let newQuestion: string;
let asked = false

let isAskModalOpen = false

let enemyNickname = $game[$enemyGameId].nickname

const setAskModalOpen = () => {
    isAskModalOpen = true
}
const setAskModalClose = () => {
    isAskModalOpen = false
}

const handleQuestionSend = (e: Event) => {
    sendTask(e, "ask_question", {
        question: newQuestion
    })
    asked = true
    setAskModalClose()
}

const handleQuestionAnswer = (e: Event, answer: "yes" | "no" | "idk") => {
    sendTask(e, "answer_question", {
        answer: answer
    })
    question.set("")
    asked = false
}
</script>

<div class="w-full flex flex-col xl:flex-row gap-x-24 border-2 border-lemon items-center py-4 px-8 xl:px-24 gap-y-4 rounded-xl">
    <Timer/>
        <div class="flex flex-row w-full gap-x-24 gap-y-4 xl:gap-y-0 items-center justify-center xl:justify-between flex-wrap text-lemon text-4xl ">
            {#if $gamePhase === "pick"}
            {#if !$pickedCharacter}
            <TextLoading>It's your time to pick a character</TextLoading>
            {:else}
            <TextLoading>{enemyNickname}&nbsp;is picking a character</TextLoading>
            {/if}
            {:else if $gamePhase === "question"}
            {#if $asking}
            {#if !asked}
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
            <TextLoading>{enemyNickname}&nbsp;is answering</TextLoading>
            {/if}
            {:else}
            {#if $question}
            <p>{enemyNickname}:&nbsp;{$question}</p>
            <div class="flex flex-row gap-2 text-black">
                <button on:click={(e) => {handleQuestionAnswer(e, "yes")}} class="bg-lemon px-4 py-1 h-fit rounded-md hover:bg-mikado">Yes!</button>
                <button on:click={(e) => {handleQuestionAnswer(e, "no")}} class="bg-lemon px-4 py-1 h-fit rounded-md hover:bg-mikado">No!</button>
                <button on:click={(e) => {handleQuestionAnswer(e, "idk")}} class="bg-lemon px-4 py-1 h-fit rounded-md hover:bg-mikado">I don't understand.</button>
            </div>
            {:else}
            <TextLoading>{enemyNickname}&nbsp;is asking</TextLoading>
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
