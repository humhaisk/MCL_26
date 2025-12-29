import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import PlayerDetails, BidTransactions, TeamDetails
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist


class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = "auction_room"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)

        player_id = data.get("player_id")
        team_code = data.get("team_name")   # CSK / MI
        current_bid = data.get("current_bid")
        transition_state = data.get("transition_state")
        transaction = await self.get_pending_transaction(player_id)

        if transaction:
            transaction.price = current_bid
            transaction.Team = await self.get_team(team_code)
            transaction.T_status = transition_state
            await self.save_transaction(transaction)
        else:
            await self.create_transaction(
                player_id, current_bid, team_code, transition_state
            )
            
        player = await self.get_player(player_id)

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
                    "wicket_keeping": "Yes" if player.WicketKeeping else "No",
                    "current_bid": current_bid,
                    "team_name": team_code,
                    "transaction_status" : transition_state,
                }
            }
        )

    async def auction_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # ================= DB METHODS =================

    @database_sync_to_async
    def get_player(self, player_id):
        try:
            return PlayerDetails.objects.get(P_ID=player_id)
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def get_pending_transaction(self, player_id):
        try:
            return BidTransactions.objects.get(playername__P_ID=player_id)
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def save_transaction(self, transaction):
        transaction.save()

    @database_sync_to_async
    def create_transaction(self, player_id, current_bid, team_code, transition_state):
        BidTransactions.objects.create(
            playername=PlayerDetails.objects.get(P_ID=player_id),
            price=current_bid,
            Team=TeamDetails.objects.get(TeamName=team_code),
            T_status=transition_state
        )
        
    @database_sync_to_async
    def get_team(self, team_code):
        try:
            return TeamDetails.objects.get(TeamName=team_code)
        except ObjectDoesNotExist:
            return None
