import { lobby, my_lobby_id } from './stores';
import type { Task, PlayerJoin, Player, PlayerStore } from '../types';

const filterObj = (obj: object, lobby_id: number) => {
	const filtered = Object.entries(obj).filter(([key, value]) => parseInt(key) !== lobby_id);
	return Object.fromEntries(filtered);
};

export const handleTask = (message: Task | PlayerJoin) => {
	let l: { [key: number]: Player } | undefined;
	lobby.subscribe((obj) => {
		l = obj;
	});

	let my_id: number | undefined;
	my_lobby_id.subscribe((id) => {
		my_id = id;
	});

	if (message.task === 'player_join') {
		delete message.task;
		if (my_id === -1) {
			my_lobby_id.set(message.player_id as number);
		}
		delete message.player_id;
		lobby.set(message);
	} else if (message.task === 'player_ready') {
		const id = message.lobby_id;
		lobby.set({
			...l,
			[id]: { ...(l as PlayerStore)[id], ready: !(l?.[id] as unknown as Player).ready }
		});
	} else if (message.task === 'player_leave') {
		lobby.set(filterObj(l as PlayerStore, message.lobby_id));
	}
};
