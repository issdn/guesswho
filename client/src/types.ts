export type Player = {
	nickname: string;
	creator: boolean;
	ready: boolean;
	game_id: number;
};

export type Task = {
	task: 'player_ready' | 'player_leave' | 'set_creator' | 'start_game';
	game_id: number;
};

export type GameTask = {
	task: 'pick_starting_character';
	game_id: number;
	character_name?: string;
	question?: string;
	answer?: string;
};

export interface PlayerJoin {
	task?: 'player_join';
	game_id?: number;
	players: [Player];
}

export type Error = {
	type: 'error';
	message: string;
	field?: string;
};

export type PlayerStore = Record<number, Player>;
