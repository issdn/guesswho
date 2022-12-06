import { phase } from './stores';
import type { PlayerJoin, Error, GameTask, LobbyTask, PlayerLeave, HelperMessage } from './types';

import * as tf from './taskFunctions';

let _phase: string;

type GenericFunctionRecord<K extends string> = Record<
	K,
	<T extends (...args: any) => void>(message: Parameters<T>) => void
>;

const lobbyTask: GenericFunctionRecord<PlayerJoin['task'] | LobbyTask['task']> = {
	start_game: tf.gameStart,
	player_ready: tf.playerReady,
	player_join: tf.playerJoin
};

const gameTask: GenericFunctionRecord<GameTask['task']> = {
	pick_starting_character: tf.startingCharacterPicked,
	guess_character: tf.characterGuessed,
	answer_question: tf.questionAnswered,
	ask_question: tf.questionAsked,
	game_end: tf.gameEnded,
	asking_overtime: tf.askingOvertime,
	answering_overtime: tf.answeringOvertime,
	characters_picked: tf.charactersPicked
};

export const handleTask = (
	message: GameTask | PlayerJoin | LobbyTask | Error | PlayerLeave | HelperMessage
) => {
	console.log(message);
	phase.subscribe((p) => (_phase = p));
	if ((message as Error).type === 'error') alert((message as Error).message);
	else if ((message as PlayerLeave).task === 'player_leave') {
		tf.playerLeave(message as PlayerLeave);
	} else if (_phase === 'lobby' || _phase === '') {
		lobbyTask[(message as LobbyTask | PlayerJoin).task](message);
	} else if (_phase === 'game') {
		gameTask[(message as GameTask).task](message);
	} else if (_phase === 'end') {
		tf.restartGame(message as HelperMessage);
	}
};
