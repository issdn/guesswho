import { enemyGameId, game, myGameId, phase, pickedCharacter } from './stores';
import type { Task, PlayerJoin, PlayerStore, Error, GameTask } from '../types';

const filterObject = (obj: object, game_id: number) => {
	const filtered = Object.entries(obj).filter(([key, value]) => parseInt(key) !== game_id);
	return Object.fromEntries(filtered);
};

let l: PlayerStore;
let _phase: string;

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

const handlegameTask = (message: Task | PlayerJoin) => {
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

export const handleGameTask = (message: GameTask) => {
	if ((message as GameTask).task === 'pick_starting_character') {
		pickedCharacter.set((message as GameTask).character_name as string);
	}
};

export const handleTask = (message: Task | PlayerJoin | GameTask | Error) => {
	console.log(message);
	phase.subscribe((p) => (_phase = p));
	if ((message as Error).type === 'error') alert((message as Error).message);
	else if (_phase === 'lobby' || _phase === '') handlegameTask(message as Task | PlayerJoin);
	else if (_phase === 'game') handleGameTask(message as GameTask);
};
