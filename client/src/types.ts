export type Player = {
	nickname: string;
	creator: boolean;
	ready: boolean;
	lobby_id: number;
};

export type Task = {
	task: 'player_ready' | 'player_leave' | 'set_creator' | 'start';
	lobby_id: number;
};

export interface PlayerJoin {
	task?: 'player_join';
	lobby_id?: number;
	players: [Player];
}

export type Error = {
	type: 'error';
	message: string;
	field?: string;
};

export type PlayerStore = Record<number, Player>;
