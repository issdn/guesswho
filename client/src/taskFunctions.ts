import { Config } from './config';
import { setAllUndready, setPlayerUndready } from './scripts';
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
	timer,
	guessing
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
		console.log((message as PlayerJoin).game_id, p.game_id);
		(message as PlayerJoin).game_id === p.game_id
			? myGameId.set(p.game_id as number)
			: enemyGameId.set(p.game_id as number);
	});
	phase.set('lobby');
};

const playerReady = (message: LobbyTask) => {
	game.subscribe((g) => (_game = g));
	enemyGameId.subscribe((_id) => (_enemyGameId = _id));
	myGameId.subscribe((_id2) => (_myGameId = _id2));
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
	enemyGameId.subscribe((id) => (_enemyGameId = id));
	sendToast(`${_game[_enemyGameId].nickname} left the game 😢`, 2500, 'warning');
	setPlayerUndready(message.new_creator_game_id);
	game.set(filterObject(_game, (message as PlayerLeave).game_id));
	enemyGameId.set(-1);
	phase.set(Config['PHASE_LOBBY']);
	resetAll();
};

const gameStart = (message: LobbyTask) => {
	phase.set(Config['PHASE_GAME']);
	gamePhase.set(Config['GAME_PHASE_PICK']);
};

/** ----------------------------- GAME TASKS ----------------------------- */

const startingCharacterPicked = (message: PickStartingCharacter) => {
	pickedCharacter.set((message as PickStartingCharacter).character_name as string);
};

const questionAsked = (message: Question) => {
	myGameId.subscribe((id) => (_myGameId = id));
	gamePhase.set(Config['GAME_PHASE_ANSWER']);
	if (message.game_id !== _myGameId) {
		question.set((message as Question).question as string);
	} else asking.set(false);
};

const questionAnswered = (message: Question) => {
	gamePhase.set(Config['GAME_PHASE_ASK']);
	answer.set((message as Question).answer as 'yes' | 'no' | 'idk');
	myGameId.subscribe((id) => (_myGameId = id));
	if (message.game_id !== _myGameId) {
		if ((message as Question).answer === 'yes' || (message as Question).answer === 'no') {
			asking.set(false);
		} else if ((message as Question).answer === 'idk') {
			asking.set(true);
		}
	} else {
		if ((message as Question).answer === 'yes' || (message as Question).answer === 'no') {
			asking.set(true);
		} else if ((message as Question).answer === 'idk') {
			asking.set(false);
			question.set('');
		}
	}
};

const characterGuessed = (message: Question) => {
	enemyGameId.subscribe((_id) => (_enemyGameId = _id));
	game.subscribe((g) => (_game = g));
	timer.refresh();
	if (message.game_id === _enemyGameId) {
		asking.set(true);
		// question.set(
		// 	`${_game[_enemyGameId].game_id} wrongly guessed a character with name ${
		// 		(message as Question).character_name as string
		// 	}`
		// );
	} else {
		asking.set(false);
		guessing.set(false);
	}
};

const charactersPicked = (message: HelperMessage) => {
	myGameId.subscribe((id) => (_myGameId = id));
	message.game_id === _myGameId ? asking.set(true) : asking.set(false);
	gamePhase.set(Config['GAME_PHASE_ASK']);
};

const gameEnded = (message: GameEnd) => {
	phase.set('end');
	gamePhase.set(Config['NONE']);
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
	setAllUndready();
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
