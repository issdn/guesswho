import { Config } from './config';
import {
	enemyGameId,
	game,
	myGameId,
	phase,
	pickedCharacter,
	question,
	asking,
	answer,
	endGameInfo,
	timer,
	gamePhase
} from './stores';
import type {
	PlayerJoin,
	PlayerStore,
	Question,
	GameEnd,
	HelperMessage,
	PickStartingCharacter,
	LobbyTask
} from './types';

const filterObject = (obj: object, game_id: number) => {
	const filtered = Object.entries(obj).filter(([key, value]) => parseInt(key) !== game_id);
	return Object.fromEntries(filtered);
};

let _game: PlayerStore;
let _enemyGameId: number;

/** ----------------------------- LOBBY TASKS ----------------------------- */

const playerJoin = (message: PlayerJoin) => {
	game.subscribe((g) => (_game = g));
	message.players.forEach((p) => {
		game.set({ ..._game, [p.game_id]: p });
		(message as PlayerJoin).game_id === p.game_id
			? myGameId.set(message.game_id as number)
			: enemyGameId.set(message.game_id as number);
	});
	phase.set('lobby');
};

const playerReady = (message: LobbyTask) => {
	game.subscribe((g) => (_game = g));
	game.set({
		..._game,
		[(message as LobbyTask).game_id]: {
			..._game[(message as LobbyTask).game_id],
			ready: !_game[(message as LobbyTask).game_id].ready
		}
	});
};

const playerLeave = (message: LobbyTask) => {
	game.set(filterObject(_game, (message as LobbyTask).game_id));
	phase.set('lobby');
};

const gameStart = (message: LobbyTask) => {
	phase.set('game');
};

/** ----------------------------- GAME TASKS ----------------------------- */

const startingCharacterPicked = (message: PickStartingCharacter) => {
	pickedCharacter.set((message as PickStartingCharacter).character_name as string);
};

const questionAsked = (message: Question) => {
	question.set((message as Question).question as string);
	timer.set(Config.ANSWERING_TIME);
};

const questionAnswered = (message: Question) => {
	answer.set((message as Question).answer as 'yes' | 'no' | 'idk');
	if ((message as Question).answer === 'yes' || (message as Question).answer === 'no') {
		let _asking;
		asking.subscribe((a) => (_asking = a));
		asking.set(!_asking);
	}
	timer.set(Config.ASKING_TIME);
};

const characterGuessed = (message: Question) => {
	asking.set(true);
	enemyGameId.subscribe((e) => (_enemyGameId = e));
	game.subscribe((g) => (_game = g));
	question.set(
		`${_game[_enemyGameId].game_id} wrongly guessed a character with name ${
			(message as Question).character_name as string
		}`
	);
};

const charactersPicked = (message: HelperMessage) => {
	let _myGameId;
	myGameId.subscribe((id) => (_myGameId = id));
	message.game_id === _myGameId ? asking.set(true) : asking.set(false);
	gamePhase.set('question');
};

const gameEnded = (message: GameEnd) => {
	phase.set('end');
	endGameInfo.set(message as GameEnd);
};

const askingOvertime = (message: HelperMessage) => {
	asking.set(false);
};

const answeringOvertime = (message: HelperMessage) => {
	asking.set(true);
};

export {
	gameStart,
	playerLeave,
	playerReady,
	playerJoin,
	characterGuessed,
	questionAnswered,
	questionAsked,
	startingCharacterPicked,
	charactersPicked,
	gameEnded,
	askingOvertime,
	answeringOvertime
};
