import { writable } from 'svelte/store';
import { handleTask } from './socket';
import { token, phase, nickname, myLobbyId } from './stores';

let _token: string;
token.subscribe((t) => (_token = t));

let _nickname: string;
nickname.subscribe((n) => {
	_nickname = n;
});

let _lobby_id: number;
myLobbyId.subscribe((id) => (_lobby_id = id));

const socket = writable();

let _socket: WebSocket;
socket.subscribe((ws) => (_socket = ws as WebSocket));

export const joinSocket = () => {
	socket.set(new WebSocket(`ws://localhost:8000/${_token}/lobby/ws`));
	_socket.onopen = (event: Event) => {
		_socket.send(JSON.stringify({ task: 'player_join', nickname: _nickname }));
	};
	_socket.onmessage = (event: MessageEvent) => {
		const message = JSON.parse(JSON.parse(event.data));
		handleTask(message);
	};
};
export const sendTask = (event: Event, taskType: string) => {
	_socket.send(
		JSON.stringify({
			task: taskType,
			lobby_id: _lobby_id
		})
	);
	event.preventDefault();
};
