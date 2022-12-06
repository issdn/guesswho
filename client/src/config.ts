export const Config = {
	BASE_URL: 'http://127.0.0.1:8000' as const,
	PICKING_TIME: 15 as const,
	ANSWERING_TIME: 15 as const,
	ASKING_TIME: 10 as const,
	ANSWER_IDK: 'idk' as const,
	ANSWER_YES: 'yes' as const,
	ANSWER_NO: 'no' as const,
	PHASE_GAME: 'game' as const,
	PHASE_LOBBY: 'lobby' as const,
	PHASE_END: 'end' as const,
	NONE: '' as const,
	GAME_PHASE_PICK: 'pick' as const,
	GAME_PHASE_QUESTION: 'question' as const
};

export type ConfigType = typeof Config;
