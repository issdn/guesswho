export const Config = {
	HOST: "127.0.0.1" as const,
	PORT: "80" as const,
	PICKING_TIME: 15 as const,
	ANSWERING_TIME: 60 as const,
	ASKING_TIME: 60 as const,
	ANSWER_IDK: 'idk' as const,
	ANSWER_YES: 'yes' as const,
	ANSWER_NO: 'no' as const,
	PHASE_GAME: 'game' as const,
	PHASE_LOBBY: 'lobby' as const,
	PHASE_END: 'end' as const,
	NONE: '' as const,
	GAME_PHASE_PICK: 'pick' as const,
	GAME_PHASE_ASK: 'ask' as const,
	GAME_PHASE_ANSWER: 'answer' as const
};

export const BASE_URL = "http://" + Config.HOST + ":" + Config.PORT

export type ConfigType = typeof Config;
