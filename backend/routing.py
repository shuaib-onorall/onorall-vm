
from django.urls import path
from myapp.consumers import  NewConsumer


channel_routing = [
    path('ws/new/',NewConsumer.as_asgi()),
]