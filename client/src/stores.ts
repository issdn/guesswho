import { readable, writable } from 'svelte/store';
import type { PlayerStore, GameEnd } from './types';

// Character picked by the player
export const pickedCharacter = writable<string>('');
// Player nickname
export const nickname = writable<string>('anonymous');
// Phase
export const baseUrl = readable<string>('http://127.0.0.1:8000');
export const phase = writable<'lobby' | 'game' | 'end' | ''>('');
export const token = writable<string>('');
export const game = writable<PlayerStore>({});
export const myGameId = writable<number>(-1);
export const enemyGameId = writable<number>(-1);
export const question = writable<string>('');
export const answer = writable<'yes' | 'no' | 'idk' | ''>('');
export const asking = writable<boolean>(false);
export const guessing = writable<boolean>(false);
export const gamePhase = writable<'picking' | 'asking' | 'answering' | ''>('');
export const endGameInfo = writable<GameEnd>();

// ----------------------- Toasts
const id = () => {
	return Math.random().toString(36).substring(2, 9);
};

export const toasts = writable<{ id: string; message: string; type: 'warning' | 'success' }[]>([]);

export const sendToast = (message: string, timeout = 4000, type: 'warning' | 'success') => {
	const toastId: string = id();
	toasts.update((state) => [...state, { id: toastId, message: message, type: type }]);
	setTimeout(() => removeToast(toastId), timeout);
};

export const removeToast = (id: string) => {
	toasts.update((all) => all.filter((t) => t.id !== id));
};
