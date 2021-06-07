from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.urls import path
import os
from channels.routing import get_default_application
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GossipBooks.settings')
django.setup()

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                   
                ]
            )
        )
    )
})
