import { enemyGameId, game, myGameId } from './stores';
import type { PlayerStore } from './types';

export const randomNumberFromRange = (min: number, max: number) => {
	return Math.floor(Math.random() * (max - min)) + min;
};

export const randomEmoji = () => {
	return String.fromCodePoint(randomNumberFromRange(128512, 128591));
};

export const prettifyCharacterName = (name: string) => {
	return name.split('_').join(' ');
};

export const setAllUndready = () => {
	let _game: PlayerStore;
	let _myGameId: number;
	let _enemyGameId: number;
	game.subscribe((_g) => (_game = _g));
	myGameId.subscribe((_id) => (_myGameId = _id));
	enemyGameId.subscribe((_id) => (_enemyGameId = _id));
	game.set({
		[_myGameId]: {
			..._game[_myGameId],
			ready: !_game[_myGameId].ready
		},
		[_enemyGameId]: {
			..._game[_enemyGameId],
			ready: !_game[_enemyGameId].ready
		}
	});
};

export const setPlayerUndready = (new_creator_game_id: number) => {
	let _game: PlayerStore;
	game.subscribe((_g) => (_game = _g));
	game.set({
		[new_creator_game_id]: {
			..._game[new_creator_game_id],
			creator: true,
			ready: false
		}
	});
};
