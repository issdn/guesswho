import { enemyLobbyId, lobby, myLobbyId, phase } from './stores';
import type { Task, PlayerJoin, PlayerStore, Error } from '../types';

const filterObject = (obj: object, lobby_id: number) => {
	const filtered = Object.entries(obj).filter(([key, value]) => parseInt(key) !== lobby_id);
	return Object.fromEntries(filtered);
};

export const handleTask = (message: Task | PlayerJoin | Error) => {
	let l: PlayerStore;
	lobby.subscribe((obj) => {
		l = obj;
	});
	if ((message as Error).type === 'error') {
		alert((message as Error).message);
	}
	if ((message as PlayerJoin).task === 'player_join') {
		(message as PlayerJoin).players.forEach((p) => {
			lobby.set({ ...l, [p.lobby_id]: p });
			(message as PlayerJoin).lobby_id === p.lobby_id
				? myLobbyId.set((message as PlayerJoin).lobby_id as number)
				: enemyLobbyId.set((message as PlayerJoin).lobby_id as number);
		});
	} else if ((message as Task).task === 'player_ready') {
		lobby.set({
			...l,
			[(message as Task).lobby_id]: {
				...l[(message as Task).lobby_id],
				ready: !l[(message as Task).lobby_id].ready
			}
		});
	} else if ((message as Task).task === 'player_leave') {
		lobby.set(filterObject(l, (message as Task).lobby_id));
	} else if ((message as Task).task === 'start') {
		console.log(message);
		phase.set('game');
	}
};
