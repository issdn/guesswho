# Main pieces of logic

1. Task - a function with a mapped string name that's being called when client sends it's name over the websocket. The structure of the message is validated by `pydantic model` (TaskModel). Every function also has a number from 1-4 which purpose is to determine whether it's message should be broadcasted, unicasted, not send at all etc. For example: function pick_character_0() is saved in an dictionary where it's string name _"pick_character"_ is the key and the value is a tuple of the function itself and it's send-type-number: `{"pick_character": (0, pick_character)}`

2. Phase - a class with multiple tasks that have the same TaskModel. It's to control the logic between multiple tasks. It has a special function naming logic (in detail in /src/phases_definitions.py commented in BasePhase).

3. player_loop - an infinite loop, where message from client is being awaited, then validated, then it's task function is being called and sent to specified players. (more in /src/phase_queue/).
     
 