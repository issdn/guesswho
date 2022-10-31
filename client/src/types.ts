export type Player = {
    nickname ? : string
    creator ? : boolean
    lobby_id ? : number
    ready ? : boolean
}

export interface Task extends Object {
    type: "task"
    task: "player_ready" | "player_leave" | "player_join" | "set_creator"
    enemy?: Player
    player?: Player
}