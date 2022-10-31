import { writable } from 'svelte/store';
import type { Task, Player, PlayerStore } from '../types';

export const token = writable<string>('');
export const lobby = writable<PlayerStore>({});
export const my_lobby_id = writable<number>(-1);
