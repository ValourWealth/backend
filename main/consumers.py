# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ObjectDoesNotExist


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]

#         if not self.user.is_authenticated:
#             await self.close()
#             return

#         self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]

#         # Validate that user exists
#         try:
#             self.other_user = await self.get_user(int(self.other_user_id))
#         except ObjectDoesNotExist:
#             await self.close()
#             return

#         self.room_name = f"chat_{min(self.user.id, self.other_user.id)}_{max(self.user.id, self.other_user.id)}"
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

#             thread = await self.get_or_create_thread(self.user, self.other_user)
#             await self.create_message(thread, self.user, message)

#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     "type": "chat_message",
#                     "message": message,
#                     "sender": self.user.username,
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
#         User = get_user_model()
#         return User.objects.get(id=user_id)

#     @database_sync_to_async
#     def get_or_create_thread(self, user1, user2):
#         from .models import ChatThread

#         if user1.profile.role == 'analyst':
#             return ChatThread.objects.get_or_create(user=user2, analyst=user1)[0]
#         else:
#             return ChatThread.objects.get_or_create(user=user1, analyst=user2)[0]

#     @database_sync_to_async
#     def create_message(self, thread, sender, content):
#         from .models import Ana_Message
#         return Ana_Message.objects.create(thread=thread, sender=sender, content=content)

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.thread_id = self.scope["url_route"]["kwargs"]["thread_id"]

        try:
            self.thread = await self.get_thread(int(self.thread_id))
        except ObjectDoesNotExist:
            await self.close()
            return

        # Only allow participants (analyst or user) to join
        if self.thread.user != self.user and self.thread.analyst != self.user:
            await self.close()
            return

        self.room_group_name = f"chat_thread_{self.thread.id}"

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

            # Save message in DB
            new_msg = await self.create_message(self.thread, self.user, message)

            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": new_msg.content,
                    "sender_id": self.user.id,
                    "timestamp": new_msg.timestamp.isoformat(),
                    "id": new_msg.id,
                }
            )
        except Exception as e:
            print("WebSocket error:", e)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "timestamp": event["timestamp"],
            "id": event["id"],
        }))

    @database_sync_to_async
    def get_thread(self, thread_id):
        from .models import ChatThread
        return ChatThread.objects.get(id=thread_id)

    @database_sync_to_async
    def create_message(self, thread, sender, content):
        from .models import Ana_Message
        return Ana_Message.objects.create(
            thread=thread,
            sender=sender,
            content=content,
            timestamp=timezone.now()  # ensure timestamp is set
        )
