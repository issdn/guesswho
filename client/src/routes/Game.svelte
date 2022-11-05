<script lang="ts">
import {
    onMount
} from "svelte";
import {token} from "./stores"

let imageNames;

onMount(() => {
    (async () => {
        await fetch(`http://127.0.0.1:8000/${$token}/characters`)
            .then((response) => response.json())
                .then((data) => imageNames = data.names)
    })()
})
</script>
