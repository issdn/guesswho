export type Player = {
	nickname: string;
	creator: boolean;
	ready: boolean;
	game_id: number;
};

export type PlayerStore = Record<number, Player>;

export type Error = {
	type: 'error';
	message: string;
	field?: string;
};

export type PlayerLeave = {
	task: 'player_leave';
	game_id: number;
	new_creator_game_id: number;
};

/* ----------- Lobby Types  ----------- */
export type LobbyTask = {
	task: 'player_ready' | 'start_game';
	game_id: number;
};

export type PlayerJoin = {
	task: 'player_join';
	game_id?: number;
	players: [Player];
};

/* ----------- Game Types  ----------- */
export type PickStartingCharacter = {
	task: 'pick_starting_character';
	character_name?: string;
	game_id: number;
};

export type Question = {
	task: 'ask_question' | 'answer_question' | 'guess_character';
	question?: string;
	answer?: 'yes' | 'no' | 'idk';
	character_name?: string;
	game_id: number;
};

export type GameEnd = {
	task: 'game_end';
	winner_id: number;
	character_name: string;
};

export type HelperMessage = {
	task: 'characters_picked' | 'asking_overtime' | 'answering_overtime' | 'restart_game';
	game_id?: number;
};

export type GameTask =
	| PickStartingCharacter
	| Question
	| GameEnd
	| (Omit<HelperMessage, 'task'> & { task: Exclude<HelperMessage['task'], 'restart_game'> });
