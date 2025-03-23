import json

from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import ChatGroup, Offer, Order

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )

        self.accept()


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        price = text_data_json['price']
        description = text_data_json['description']
        offer = Offer.objects.create(
            price=price,
            proposer=self.user,
            description=description,
            group=self.chatroom,
        )

        event = {
            'type': 'message_handler',
            'message_id': offer.offer_id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = get_object_or_404(Offer, offer_id=message_id)
        html = render_to_string('orders/partials/chat_message_p.html', context={
            'message': message,
            'user': self.user,
        })
        self.send(text_data=html)

        # Update buttons after sending the message

        event = {
            'type': 'make_buttons_visible',
            'visible': False if message.proposer == self.user else True,
            'offer_id': message.offer_id if message else None,  # Include the offer ID if available
        }
        self.make_buttons_visible(event)


    def make_buttons_visible(self, event):
        visible = event['visible']
        offer_id = event.get('offer_id')

        html = render_to_string('orders/partials/accept_offer_buttons.html', context={
            'visible': visible,
            'offer_id': offer_id,
        })
        self.send(text_data=html)


