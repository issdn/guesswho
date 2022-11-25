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
	character_name?: string;
	game_id: number;
	task: 'pick_starting_character';
};

export type QuestionAsk = {
	task: 'ask_question' | 'answer_question' | 'guess_character';
	question?: string;
	answer?: 'yes' | 'no' | 'idk';
	character_name?: string;
};

export type PlayerJoin = {
	task?: 'player_join';
	game_id?: number;
	players: [Player];
};

export type GameEnd = {
	task: 'game_end';
	winner_id: number;
	character_name: string;
	restart: boolean;
};

export type Error = {
	type: 'error';
	message: string;
	field?: string;
};

export type PlayerStore = Record<number, Player>;
