from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        
        if user.is_anonymous:
            await self.close()
        else:
            await self.accept()

    async def disconnect(self, code):
        await super().disconnect(code)