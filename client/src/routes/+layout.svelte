<script lang="ts">
    import "../app.css";
    import wave from "$lib/assets/wave.svg"
</script>

<img src={wave} class="absolute top-0 left-0 -z-[5] h-screen w-full object-cover" alt="scene blob"/>
<div class="w-full h-full font-['Mouse_Memoirs'] p-8">
    <slot />
</div>