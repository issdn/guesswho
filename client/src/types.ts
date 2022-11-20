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
	task: 'ask_question' | 'answer_question';
	question: string;
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
