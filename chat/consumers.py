import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Thread, ChatMessage, Online

class ChatConsumer(AsyncConsumer):
    async  def websocket_connect(self, event):
        print("connected", event)
       
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        print(other_user, me)
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        print(me, thread_obj.id)
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.Iss_active1(me)

        await self.send({
            "type": "websocket.accept"
        })

        # await asyncio.sleep(10)
        # await self.send({
        #     "type" : "websocket.send",
        #     "text" : 'hello world'
        # })
        #when it's receive
    async  def websocket_receive(self, event):
        print("receive", event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            print(msg)
            user = self.scope['user']
            theUser = str(user)
            username = 'default'
            if user.is_authenticated:
                username = user.username
            myResponse = {
                'message' : msg,
                'username' : username,
                
            }

            await self.create_chat_message(user, msg)
            
            print(self)
            #broadcasts the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(myResponse)
                }
            )
        #when it's disconnected
    async  def chat_message(self, event):
       #sends the actual message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })



    async  def websocket_disconnect(self, event):
        user = self.scope['user']
        await self.Iss_active(user)
        print("disconnect", event)



    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]
    @database_sync_to_async
    def Iss_active(self, user):
        userT = User.objects.get(id=user.id)
        userT.status.status = False
        userT.status.save()
        return  userT

    @database_sync_to_async
    def Iss_active1(self, user):
        userT = User.objects.get(id=user.id)
        userT.status.status = True
        userT.status.save()
        return  userT
    @database_sync_to_async
    def create_chat_message(self, user, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=user, message=msg)