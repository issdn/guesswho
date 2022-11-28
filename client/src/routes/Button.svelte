<script lang="ts">
    export let onClickFunc: (e: Event) => void;
    export let disabled: boolean = false;
    export let style: string = ""
</script>

<button class="capitalize {style} bg-lemon rounded-3xl px-16 py-1 text-2xl text-space cursor-{disabled ? 'default':'pointer'}" disabled={disabled} on:click={onClickFunc}>
    <slot/>
</button>