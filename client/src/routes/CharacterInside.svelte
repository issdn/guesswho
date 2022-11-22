<script lang="ts">
export let characterName: string = "";
export let url: string = "";
</script>

<div class="w-full h-full transition-transform duration-1000 preserve3d">
    <div class="absolute bg-safety backface-hidden rotate-y-0">
        <img src={url} alt="character" class="border-2 border-black">
        <p class="text-lg sm:text-xl text-center my-[.15rem]">{characterName}</p>
    </div>
    <div class="absolute h-full w-full backface-hidden bg-safety flip-y">
        <div class="relative h-full w-full">
            <p class="absolute left-[50%] top-[50%] -translate-y-1/2 -translate-x-1/2 rotate-12 text-[10rem] opacity-10">?</p>
            <p class="absolute left-[50%] top-[50%] -translate-y-1/2 -translate-x-1/2 text-3xl text-center">{characterName}</p>
        </div>
    </div>
</div>
