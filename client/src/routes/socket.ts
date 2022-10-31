import {player, enemy} from "./stores"
import type {Task, Player} from "../types"

export const handleTask = (message: Task) => {
    if (message.task === "player_join") {
        player.set(message.player as Player);
        if(message.enemy){
            enemy.set(message.enemy)
        }
    } else if (message.task === "player_ready") {
        if(message.player){
            player.set(message.player);
        } else if(message.enemy) {
            enemy.set(message.enemy)
        }
    }
}