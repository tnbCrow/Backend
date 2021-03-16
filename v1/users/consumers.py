from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']

        if user.is_anonymous:
            await self.close()
        else:
            self.chat_room_name = self.scope['url_route']['kwargs']['chat_room']
            self.chat_group_name = f"chat_group_{self.chat_room_name}"

            # Join room group
            await self.channel_layer.group_add(
                group=self.chat_group_name,
                channel=self.channel_name,
            )            
            print("1:",self.chat_group_name)
            await self.accept()

    # Receive message from WebSocket client
    async def receive_json(self, content, **kwargs):
        print("got message")
        print(self.chat_group_name)
        message_type = content.get('type')

        #send the message to the group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': content.get('message'),
            }
        )

    # Receive message from the group
    async def chat_message(self,message):
        #send message to the client
        await self.send_json(message)

    async def disconnect(self, code):
        await super().disconnect(code)
