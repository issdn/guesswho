<script lang="ts">
    import {timer} from "../stores"
    let time = $timer
    
    setInterval(() => {
        if (time > 0) time--;
    }, 1000);

</script>

<p class="text-7xl text-lemon">
    {time}
</p>