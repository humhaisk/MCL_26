import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = "auction_room"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Data received:", data)

        # SEND TO ALL CONNECTED CLIENTS
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "auction_message",
                "data": data
            }
        )

    async def auction_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
