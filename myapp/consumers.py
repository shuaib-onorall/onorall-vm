from channels.generic.websocket import AsyncJsonWebsocketConsumer  #web socket is used for full duplex communication between client and server
from asgiref.sync import async_to_sync                         #it will convert the asynchronous into synchronous
import json
class NewConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('fffffffffffffffffffffff')
        await self.accept()
        await self.send(text_data=json.dumps({'status':'connected from new conswswssumer'}))

    async def receive(self,text_data):
        print(text_data)
        await self.send(text_data=json.dumps(text_data))
    
    async def disconnect(self,*args,**kwargs):
        print('disconnect')


class Notifyconsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('fffffffffffffffffffffff')
        self.group_name = 'gossip'
        await self.channel_layer.group_add(self.group_name ,self.channel_name)
        await self.accept()
        print(f"Added{self.channel_name} channel to gossip")

    async def disconnect(self,*args,**kwargs):
        print('fffffffffffffffffffffff' , 'disconnect') 
        await self.channel_layer.group_discard( self.group_name ,self.channel_name)
        print(f"Removed{self.channel_name} channel from gossip")

    async def new_notice(self,event):
        await self.send_json(event)
        print(f"Got message{event} at {self.channel_name}")


    async def send_notification(self , event):
        print('func working-----------')
        




## game/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

# class TicTacToeConsumer(AsyncJsonWebsocketConsumer):

#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_code']
#         self.room_group_name = 'room_%s' % self.room_name

#         # Join room group
#     async def send_notification(self,event):
#         print(event)
#         await self.send(text_data=json.dumps(event))
#        # print('working______________')

# # class NotificationCosumer(AsyncJsonWebsocketConsumer):
# #     async def connect(self):
# #         self.room_name=self.scope['url']['kwargs']['room_name']
# #         self.room_group_name='notification_%s'%self.room_name

# #         await self.channel_layer.group_add(
# #             self.room_group_name,
# #             self.channel_name
# #         )
# #         await self.accept()

# #     async def disconnect(self, close_code):
# #         print("Disconnected")
# #         # Leave room group
# #         await self.channel_layer.group_discard(
# #             self.room_group_name,
# #             self.channel_name
# #         )

# #         print(close_code)

# #     async def receive(self, text_data):
# #         """
# #         Receive message from WebSocket.
# #         Get the event and send the appropriate event
# #         """
# #         response = json.loads(text_data)
# #         event = response.get("event", None)
# #         message = response.get("message", None)
# #         if event == 'MOVE':
# #             # Send message to room group
# #             await self.channel_layer.group_send(self.room_group_name, {
# #                 'type': 'send_message',
# #                 'message': message,
# #                 "event": "MOVE"
# #             })

# #         if event == 'START':
# #             # Send message to room group
# #             await self.channel_layer.group_send(self.room_group_name, {
# #                 'type': 'send_message',
# #                 'message': message,
# #                 'event': "START"
# #             })

# #         if event == 'END':
# #             # Send message to room group
# #             await self.channel_layer.group_send(self.room_group_name, {
# #                 'type': 'send_message',
# #                 'message': message,
# #                 'event': "END"
# #             })
# #         print('events' ,event)
# #         print('response ' ,response)

# #     async def send_message(self, res):
# #         """ Receive message from room group """
# #         # Send message to WebSocket
# #         print(res)
# #         await self.send(text_data=json.dumps({
# #             "payload": res,
# #         }))
# #     #async def send_notification(self,event):
# #        # message=event['message']
# #         #await self.send(text_data=json.dumps({
# #         #    'message':message
# #         #}))
