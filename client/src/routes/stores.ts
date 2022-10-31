import { writable } from 'svelte/store';
import type {Task, Player} from "../types"


export const token = writable<string>("");
export const player = writable<Player>({nickname: "anonymous", lobby_id: -1, creator: false, ready: false})
export const enemy = writable<Player>({nickname: "anonymous", lobby_id: -1, creator: false, ready: false})