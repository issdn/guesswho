<script lang="ts">
    export let modalOpen: boolean;
    export let closeModal: () => void;
</script>

{#if modalOpen}
<div class="fixed top-0 left-0 w-screen h-screen flex flex-col justify-center content-center z-20">
    <div class="flex flex-row justify-center">
        <div class="bg-secondaryYellow w-96 h-96 flex flex-col gap-8 py-8 px-16 rounded-xl z-[21]">
            <slot/>
        </div>
    </div>
    <div on:mousedown={closeModal} class="top-0 left-0 fixed bg-black opacity-75 w-full h-full"></div>
</div>
{/if}