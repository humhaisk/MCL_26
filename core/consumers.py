from channels.consumer import AsyncConsumer 
from channels.exceptions import StopConsumer 
import json 

class MyConsumer(AsyncConsumer): 
    async def websocket_connect(self, event): 
        await self.channel_layer.group_add("bidders", self.channel_name) 
        await self.send({ "type": "websocket.accept" }) 
    
    async def websocket_receive(self, text_data): 
        if isinstance(text_data, dict):
            data = text_data
        else:
            data = json.loads(text_data)

        team_name = data.get("team_name")
        current_bid = data.get("current_bid")
        player_id = data.get("player_id")
        
        await self.channel_layer.group_send (
            'bidders', 
            {
            "type": "broadcast_bid",
            "team_name": team_name,
            "current_bid": current_bid,
            "player_id": player_id
            }
        )
        print("Data processed and response sent.", data)

    async def websocket_disconnect(self, event): 
        await self.channel_layer.group_discard("bidders", self.channel_name)
        raise StopConsumer()