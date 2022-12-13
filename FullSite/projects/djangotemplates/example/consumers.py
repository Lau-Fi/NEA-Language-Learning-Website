# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer

#The consumers.py is used for connecting to the chatroom. 

class ChatConsumer(AsyncWebsocketConsumer): #Class chat consumer is defined with the websocket consumer import libarary passed into it.
    async def connect(self): #Connects its self (self) by using an asnyc definition
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"] #the self.room_name current instance of the class Chatconsumer is set to equal to the local scope of the function. Passed in is the url route, the keyword arguement and the room_name. 
        self.room_group_name = "chatrooms_%s" % self.room_name #the room name group will have chatrooms concatanated onto the url along with the room name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name) # The channel layer connects the group name and the channel name

        await self.accept() #Accepts an incomming connection from a TCP client.

    async def disconnect(self, close_code): #To disconnect it discards the group and channel name
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data): #This async definition recives the message
        text_data_json = json.loads(text_data) 
        message = text_data_json["message"] #Stores the message as a json string

        # Send message to room group
        await self.channel_layer.group_send( #Sends the message to the group, the type is a chat message. The below line is JSON
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message})) #Awaits the json text to be sent. The messange is stored in the variable "message"

