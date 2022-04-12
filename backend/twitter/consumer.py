import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    groups = ["general"]

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("message", self.channel_name)

    async def send_info_to_user_group(self, event):
        message = event["text"]
        await self.send(text_data=json.dumps(message))

    async def send_last_message(self, event):
        last_msg = await self.get_last_message(301209643)
        last_msg["status"] = event["text"]
        await self.send(text_data=json.dumps(last_msg))

    @database_sync_to_async
    def get_last_message(self, user_id):
        return {"status": "some message"}
