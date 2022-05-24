"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from myapp.consumers import *
import django
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from django.conf.urls import url
from myapp.consumers import  NewConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
application = get_asgi_application()

websocket_urlpatterns = [
    path('ws/new/',NewConsumer.as_asgi()),
    path('ws/notice/',Notifyconsumer.as_asgi())
]

application = ProtocolTypeRouter({ 

    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        } )
    



# #____________________________________________________:)
# application = ProtocolTypeRouter({"https": get_asgi_application})
