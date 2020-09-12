import json
from websocket_server import WebsocketServer
from unity_response_data import UnityResponseData


class UnityWebSocket:
	def __init__(self, port):
		print("Creating Unity socket")
		self.server = WebsocketServer(port)
		self.server.set_fn_new_client(self.new_client)
		self.server.set_fn_message_received(self.on_message)

		self.on_play_mode_state_changed = self.event_default
		self.on_pause_mode_state_changed = self.event_default
		self.on_set_state = self.event_default

	def start(self):
		self.server.run_forever()

	def new_client(self, client, ws):
		self.send("open-socket")

	def on_message(self, client, ws, message):
		print(message)
		data = UnityResponseData(message)

		{
			"setState": self.on_set_state,
			"playModeStateChanged": self.on_play_mode_state_changed,
			"pauseModeStateChanged": self.on_pause_mode_state_changed
		}.get(data.event, self.event_default)(data)

	def send(self, action, context=None, settings=None, state=0):
		if len(self.server.clients) == 0:
			return False

		data = {
			"action": action,
			"context": context,
			"settings": settings,
			"state": state
		}

		self.server.send_message_to_all(json.dumps(data))
		return True

	def event_default(self, data):
		pass
