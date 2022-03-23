from channels.generic.websocket import AsyncJsonWebsocketConsumer  #web socket is used for full duplex communication between client and server
from channels.generic.websocket import WebsocketConsumer  
from asgiref.sync import async_to_sync                         #it will convert the asynchronous into synchronous
import json


class NewConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'status':'connected from new consumer'}))

    async def receive(self,text_data):
        print(text_data)
        await self.send(text_data=json.dumps(text_data))
    
    async def disconnect(self,*args,**kwargs):
        print('disconnect')
        

class Notifyconsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'gossip'
        
        await self.channel_layer.group_add(self.group_name ,self.channel_name)
        await self.accept()
        print(f"Added{self.channel_name} channel to gossip")

    async def disconnect(self,*args,**kwargs):
        await self.channel_layer.group_discard( self.group_name ,self.channel_name)
        print(f"Removed{self.channel_name} channel from gossip")

    async def new_notice(self,event):
        await self.send_json(event)
        print(f"Got message{event} at {self.channel_name}")

class NotificationCosumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url']['kwargs']['room_name']
        self.room_group_name='notification_%s'%self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def send_notification(self,event):
        message=event['message']
        await self.send(text_data=json.dumps({
            'message':message
        }))