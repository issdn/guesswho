<script lang="ts">
    export let time: number;

    setInterval(() => {
        if (time > 0) time--;
    }, 1000);

</script>

<p class="text-7xl text-lemon">
    {time}
</p>