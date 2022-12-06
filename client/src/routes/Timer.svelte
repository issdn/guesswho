<script lang="ts">
	import { Config } from "../config";
    import {timer, gamePhase} from "../stores"
    
    $:  if($gamePhase === "ask") timer.setNew(Config.ASKING_TIME)
        else if($gamePhase === "answer") timer.setNew(Config.ANSWERING_TIME)

    setInterval(() => {
		if ($timer > 0) timer.decrement();
	}, 1000);
</script>

<p class="text-7xl text-lemon">
    {$timer}
</p>