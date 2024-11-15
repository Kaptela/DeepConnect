import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        __room_name = str(self.scope['url_route']['kwargs']['room_name']).split('_')
        __room_name.sort()
        self.room_name = '_'.join(__room_name)
        
        self.room_group_name = f"chat_{self.room_name}"

        # Проверка авторизации пользователя (если требуется)
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        # Добавление в группу
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Удаление из группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        time = text_data_json["time"]

        # Отправка сообщения в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "time": time,
            }
        )

    async def chat_message(self, event):
        # Отправка сообщения клиенту
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "time": event["time"],
        }))
