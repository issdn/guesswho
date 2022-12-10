<script lang="ts">
	export let onClickFunc: () => void;
	export let style: string = '';
</script>

<div
	on:click={onClickFunc}
	on:keypress={onClickFunc}
	on:keydown={onClickFunc}
	class="relative h-10 w-10
    cursor-pointer
    rounded-xl 
    before:absolute before:left-1/2 
    before:top-1/2 
    before:h-1 
    before:w-8 
    before:-translate-x-1/2 
    before:-translate-y-1/2 
    before:rotate-45 
    before:rounded-xl 
    before:bg-gray-100 before:content-['']
    after:absolute
    after:left-1/2
    after:top-1/2
    after:h-1
    after:w-8 
    after:-translate-x-1/2 
    after:-translate-y-1/2
    after:-rotate-45
    after:rounded-xl
    after:bg-gray-100
    after:content-['']
    {style}
    "
/>
