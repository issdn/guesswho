export type Player = {
	nickname: string;
	creator: boolean;
	ready: boolean;
};

export type Task = {
	task: 'player_ready' | 'player_leave' | 'set_creator';
	lobby_id: number;
};

export interface PlayerJoin {
	task?: 'player_join';
	player_id?: number;
	[key: number]: Player;
}

export type Error = {
	type: 'error';
	message: string;
	field?: string;
};

export type PlayerStore = { [key: number]: Player };
