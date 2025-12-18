import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import PlayerDetails
from channels.db import database_sync_to_async

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

        player = await self.get_player(data.get("player_id"))

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "auction_message",
                "data": {
                    "player_id": player.P_ID,
                    "name": player.Name,
                    "dept": player.Dept,
                    "batch": player.Batch,
                    "photo_url": player.PlayerPhoto.url if player.PlayerPhoto else "",
                    "role": player.PlayerRole,
                    "wicket_keeping": player.WicketKeeping,
                    "current_bid": data.get("current_bid"),
                    "team_code": data.get("team_code"),
                }
            }
        )

    async def auction_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_player(self, player_id):
        return PlayerDetails.objects.get(P_ID=player_id)
