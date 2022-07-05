# """
# ASGI config for backend project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
# """

import os

from django.core.asgi import get_asgi_application
from channels.routing import URLRouter , ProtocolTypeRouter
from django.urls import path
from myapp.consumers import *
import django
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from django.conf.urls import url
from myapp.consumers import  NewConsumer
from channels.security.websocket import AllowedHostsOriginValidator
from .routing import channel_routing
from channels.routing import get_default_application



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()


#application = get_default_application()
# this gave me error in docker(upper-line) when we connect to socket url using websocket-king :   instance = application(scope) | TypeError: 'list' object is not callable
    


application = ProtocolTypeRouter({"websocket": AuthMiddlewareStack(URLRouter(channel_routing))})
# application = ProtocolTypeRouter({"websocket": AuthMiddlewareStack(URLRouter(channel_routing))}) 
# and this application = ProtocolTypeRouter({"websocket": (URLRouter(channel_routing))})
# and this application = AuthMiddlewareStack(ProtocolTypeRouter({"websocket": URLRouter(channel_routing)}))
# and this application = ProtocolTypeRouter({"websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(channel_routing)))}) 
#this gave me error in docker when we connect url to using websocket king but this *** (: showing connected and disconnect :) *** : |     for res in _socket.getaddrinfo(host, port, family, type, proto, flags): | socket.gaierror: [Errno -2] Name or service not known



# # #____________________________________________________:)
# # application = ProtocolTypeRouter({"https": get_asgi_application})
# # run daphne serrver
# # daphne -b 0.0.0.0 -p 8000 backend.asgi:application


# import os
# import django
# from channels.layers import get_channel_layer
# from channels.routing import get_default_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# channel_layer = get_channel_layer()