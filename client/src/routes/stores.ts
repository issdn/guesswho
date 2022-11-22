import { readable, writable } from 'svelte/store';
import type { PlayerStore } from '../types';

// Character picked by the player
export const pickedCharacter = writable<string>('');
// Player nickname
export const nickname = writable<string>('anonymous');
// Phase
export const phase = writable<'lobby' | 'game' | ''>('');
export const token = writable<string>('');
export const game = writable<PlayerStore>({});
export const myGameId = writable<number>(-1);
export const enemyGameId = writable<number>(-1);
export const baseUrl = readable<string>('http://127.0.0.1:8000');
export const question = writable<string>('');
export const answer = writable<'yes' | 'no' | 'idk' | ''>('');
export const asking = writable<boolean>(false);
export const gamePhase = writable<'picking' | 'asking' | 'answering' | ''>('');
