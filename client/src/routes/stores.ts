import { writable } from 'svelte/store';
import type { PlayerStore } from '../types';

export const pickedCharacter = writable<string>('');
export const nickname = writable<string>('anonymous');
export const phase = writable<'lobby' | 'game' | ''>('');
export const token = writable<string>('');
export const game = writable<PlayerStore>({});
export const myGameId = writable<number>(-1);
export const enemyGameId = writable<number>(-1);
