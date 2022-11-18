import { writable } from 'svelte/store';
import { handleGameTask, handleTask } from './socket';
import { token, phase, nickname, myGameId } from './stores';

let _phase: string;

let _token: string;
token.subscribe((t) => (_token = t));

let _nickname: string;
nickname.subscribe((n) => {
	_nickname = n;
});

let _game_id: number;
myGameId.subscribe((id) => (_game_id = id));

const socket = writable();

let _socket: WebSocket;
socket.subscribe((ws) => (_socket = ws as WebSocket));

export const joinSocket = () => {
	socket.set(new WebSocket(`ws://localhost:8000/${_token}/game/ws`));
	_socket.onopen = (event: Event) => {
		_socket.send(JSON.stringify({ task: 'player_join', nickname: _nickname }));
	};
	_socket.onmessage = (event: MessageEvent) => {
		const message = JSON.parse(JSON.parse(event.data));
		handleTask(message);
	};
};

export const sendTask = (
	event: Event,
	taskType: string,
	other: Record<string, string | number | boolean> = {}
) => {
	_socket.send(
		JSON.stringify({
			task: taskType,
			game_id: _game_id,
			...other
		})
	);
	event.preventDefault();
};
