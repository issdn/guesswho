import {
	enemyGameId,
	game,
	myGameId,
	phase,
	pickedCharacter,
	question,
	asking,
	answer,
	endGameInfo
} from './stores';
import type {
	Task,
	PlayerJoin,
	PlayerStore,
	Error,
	GameTask,
	QuestionAsk,
	GameEnd,
	HelperMessage
} from './types';

const filterObject = (obj: object, game_id: number) => {
	const filtered = Object.entries(obj).filter(([key, value]) => parseInt(key) !== game_id);
	return Object.fromEntries(filtered);
};

let l: PlayerStore;
let _phase: string;

let _enemyGameId: number;

function playerJoin(message: PlayerJoin) {
	game.subscribe((_l) => (l = _l));
	message.players.forEach((p) => {
		game.set({ ...l, [p.game_id]: p });
		(message as PlayerJoin).game_id === p.game_id
			? myGameId.set(message.game_id as number)
			: enemyGameId.set(message.game_id as number);
	});
	phase.set('lobby');
}

const playerReady = (message: Task) => {
	game.subscribe((_l) => (l = _l));
	game.set({
		...l,
		[(message as Task).game_id]: {
			...l[(message as Task).game_id],
			ready: !l[(message as Task).game_id].ready
		}
	});
};

const handleLobbyTask = (message: Task | PlayerJoin) => {
	if ((message as PlayerJoin).task === 'player_join') {
		playerJoin(message as PlayerJoin);
	} else if ((message as Task).task === 'player_ready') {
		playerReady(message as Task);
	} else if ((message as Task).task === 'player_leave') {
		game.set(filterObject(l, (message as Task).game_id));
	} else if ((message as Task).task === 'start_game') {
		phase.set('game');
	}
};

export const handleGameTask = (message: GameTask | QuestionAsk | GameEnd | HelperMessage) => {
	if ((message as GameTask).task === 'pick_starting_character') {
		pickedCharacter.set((message as GameTask).character_name as string);
	} else if ((message as QuestionAsk).task === 'ask_question') {
		question.set((message as QuestionAsk).question as string);
	} else if ((message as QuestionAsk).task === 'answer_question') {
		answer.set((message as QuestionAsk).answer as 'yes' | 'no' | 'idk');
		if ((message as QuestionAsk).answer === 'yes' || (message as QuestionAsk).answer === 'no') {
			let _asking;
			asking.subscribe((a) => (_asking = a));
			asking.set(!_asking);
		}
	} else if ((message as QuestionAsk).task === 'guess_character') {
		asking.set(true);
		enemyGameId.subscribe((e) => (_enemyGameId = e));
		game.subscribe((g) => (l = g));
		question.set(
			`${l[_enemyGameId].game_id} wrongly guessed a character with name ${
				(message as QuestionAsk).character_name as string
			}`
		);
	} else if ((message as GameEnd).task === 'game_end') {
		phase.set('end');
		endGameInfo.set(message as GameEnd);
	} else if ((message as HelperMessage).task === 'asking_overtime') {
		asking.set(false);
	} else if ((message as HelperMessage).task === 'answering_overtime') {
		asking.set(true);
	}
};

export const handleTask = (
	message: Task | PlayerJoin | GameTask | Error | QuestionAsk | HelperMessage
) => {
	console.log(message);
	phase.subscribe((p) => (_phase = p));
	if ((message as Error).type === 'error') alert((message as Error).message);
	else if (_phase === 'lobby' || _phase === '') handleLobbyTask(message as Task | PlayerJoin);
	else if (_phase === 'game')
		handleGameTask(message as GameTask | QuestionAsk | GameEnd | HelperMessage);
};
