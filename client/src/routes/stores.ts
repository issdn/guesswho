import { writable } from 'svelte/store';
import type { PlayerStore } from '../types';

export const nickname = writable<string>('anonymous');
export const phase = writable<'lobby' | 'game' | ''>('');
export const token = writable<string>('');
export const lobby = writable<PlayerStore>({});
export const myLobbyId = writable<number>(-1);
export const enemyLobbyId = writable<number>(-1);
