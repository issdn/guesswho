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
	gameEndInfo,
	gamePhase,
	sendToast,
	resetAll,
	timer
} from './stores';
import type {
	PlayerJoin,
	PlayerStore,
	Question,
	GameEnd,
	HelperMessage,
	PickStartingCharacter,
	LobbyTask,
	PlayerLeave
} from './types';

const filterObject = (obj: object, game_id: number) => {
	const filtered = Object.entries(obj).filter(([key, value]) => parseInt(key) !== game_id);
	return Object.fromEntries(filtered);
};

let _game: PlayerStore;
let _enemyGameId: number;
let _myGameId: number;

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

const playerLeave = (message: PlayerLeave) => {
	game.subscribe((g) => (_game = g));
	game.set({
		..._game,
		[(message as PlayerLeave).new_creator_game_id]: {
			..._game[(message as PlayerLeave).new_creator_game_id],
			creator: true,
			ready: false
		}
	});
	enemyGameId.subscribe((id) => (_enemyGameId = id));
	sendToast(`${_game[_enemyGameId].nickname} left the game 😢`, 2500, 'warning');
	game.set(filterObject(_game, (message as PlayerLeave).game_id));
	enemyGameId.set(-1);
	phase.set('lobby');
	resetAll();
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
	gamePhase.set(Config['GAME_PHASE_ANSWER']);
};

const questionAnswered = (message: Question) => {
	answer.set((message as Question).answer as 'yes' | 'no' | 'idk');
	if ((message as Question).answer === 'yes' || (message as Question).answer === 'no') {
		let _asking;
		asking.subscribe((a) => (_asking = a));
		asking.set(!_asking);
	}
	gamePhase.set(Config['GAME_PHASE_ASK']);
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
	myGameId.subscribe((id) => (_myGameId = id));
	message.game_id === _myGameId ? asking.set(true) : asking.set(false);
	gamePhase.set(Config['GAME_PHASE_ASK']);
};

const gameEnded = (message: GameEnd) => {
	phase.set('end');
	gameEndInfo.set(message as GameEnd);
};

const askingOvertime = (message: HelperMessage) => {
	myGameId.subscribe((id) => (_myGameId = id));
	if (_myGameId === message.game_id) {
		asking.set(false);
	} else {
		asking.set(true);
	}
	timer.refresh();
};

const answeringOvertime = (message: HelperMessage) => {
	myGameId.subscribe((id) => (_myGameId = id));
	if (_myGameId === message.game_id) {
		asking.set(false);
		question.set('');
	} else {
		asking.set(true);
	}
	timer.refresh();
};

const restartGame = (message: HelperMessage) => {
	phase.set('lobby');
	resetAll();
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
	answeringOvertime,
	restartGame
};
