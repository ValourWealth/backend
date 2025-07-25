# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model



# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]

#         if not self.user.is_authenticated:
#             await self.close()
#             return

#         self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
#         self.room_name = f"chat_{min(self.user.id, int(self.other_user_id))}_{max(self.user.id, int(self.other_user_id))}"
#         self.room_group_name = f"chat_{self.room_name}"

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#         print(f"[WebSocket Disconnected] code={close_code} user={self.user.username}")

#     async def receive(self, text_data):
#         try:
#             data = json.loads(text_data)
#             message = data.get("message")
#             if not message:
#                 return

#             sender = self.user
#             receiver = await self.get_user(int(self.other_user_id))

#             thread = await self.get_or_create_thread(sender, receiver)
#             await self.create_message(thread, sender, message)

#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     "type": "chat_message",
#                     "message": message,
#                     "sender": sender.username,
#                 }
#             )
#         except Exception as e:
#             print("WebSocket error:", e)

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             "message": event["message"],
#             "sender": event["sender"],
#         }))

#     @database_sync_to_async
#     def get_user(self, user_id):
#         from django.contrib.auth import get_user_model
#         User = get_user_model()
#         return User.objects.get(id=user_id)


#     @database_sync_to_async
#     def get_or_create_thread(self, user1, user2):
#         from .models import ChatThread  # ✅ moved inside method

#         if user1.profile.role == 'analyst':
#             return ChatThread.objects.get_or_create(user=user2, analyst=user1)[0]
#         else:
#             return ChatThread.objects.get_or_create(user=user1, analyst=user2)[0]

#     @database_sync_to_async
#     def create_message(self, thread, sender, content):
#         from .models import Ana_Message  # ✅ moved inside method
#         return Ana_Message.objects.create(thread=thread, sender=sender, content=content)

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]

        # Validate that user exists
        try:
            self.other_user = await self.get_user(int(self.other_user_id))
        except ObjectDoesNotExist:
            await self.close()
            return

        self.room_name = f"chat_{min(self.user.id, self.other_user.id)}_{max(self.user.id, self.other_user.id)}"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"[WebSocket Disconnected] code={close_code} user={self.user.username}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")
            if not message:
                return

            thread = await self.get_or_create_thread(self.user, self.other_user)
            await self.create_message(thread, self.user, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": self.user.username,
                }
            )
        except Exception as e:
            print("WebSocket error:", e)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        User = get_user_model()
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_or_create_thread(self, user1, user2):
        from .models import ChatThread

        if user1.profile.role == 'analyst':
            return ChatThread.objects.get_or_create(user=user2, analyst=user1)[0]
        else:
            return ChatThread.objects.get_or_create(user=user1, analyst=user2)[0]

    @database_sync_to_async
    def create_message(self, thread, sender, content):
        from .models import Ana_Message
        return Ana_Message.objects.create(thread=thread, sender=sender, content=content)
