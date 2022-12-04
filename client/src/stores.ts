import { writable } from 'svelte/store';
import type { PlayerStore, GameEnd } from './types';
import { Config, type ConfigType } from './config';

/** Character picked by the player  */
export const pickedCharacter = writable<string>('');
/** Player nickname  */
export const nickname = writable<string>('anonymous');
/** Secret token to join the game  */
export const token = writable<string>('');
/** Obj storing info about all players  */
export const game = writable<PlayerStore>({});
/** Client game id  */
export const myGameId = writable<number>(-1);
/** Game if of other players  */
export const enemyGameId = writable<number>(-1);
/** Stored question from the enemy  */
export const question = writable<string>('');
/** Stored answer from the enemy  */
export const answer = writable<
	ConfigType['ANSWER_IDK'] | ConfigType['NONE'] | ConfigType['ANSWER_YES'] | ConfigType['ANSWER_NO']
>('');
/** Stored to determine wheter the player should be asking or answering now.  */
export const asking = writable<boolean>(false);
/** Mainly to determine what event handlers should the cards have.  */
export const guessing = writable<boolean>(false);
/** Phase needed for determining what view to render  */
export const phase = writable<
	| ConfigType['PHASE_LOBBY']
	| ConfigType['PHASE_GAME']
	| ConfigType['PHASE_END']
	| ConfigType['NONE']
>('');
/** Necessary to determine which text to show in the info bar on top. */
export const gamePhase = writable<
	ConfigType['GAME_PHASE_QUESTION'] | ConfigType['GAME_PHASE_PICK']
>('pick');
/** Stats and info at the end of the game.  */
export const endGameInfo = writable<GameEnd>();

/** Keeps time of picking a character, asking, answering etc. */
export const timer = writable<
	ConfigType['PICKING_TIME'] | ConfigType['ANSWERING_TIME'] | ConfigType['ASKING_TIME']
>(Config.PICKING_TIME);

/** ------------------ Toasts ------------------ */
const id = () => {
	return Math.random().toString(36).substring(2, 9);
};

/** Popup notifications/errors */
export const toasts = writable<{ id: string; message: string; type: 'warning' | 'success' }[]>([]);

export const sendToast = (message: string, timeout = 4000, type: 'warning' | 'success') => {
	const toastId: string = id();
	toasts.update((state) => [...state, { id: toastId, message: message, type: type }]);
	setTimeout(() => removeToast(toastId), timeout);
};

export const removeToast = (id: string) => {
	toasts.update((all) => all.filter((t) => t.id !== id));
};
