from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.urls import path
import os
from django.core.asgi import get_asgi_application
from messaging.consumers import (ChatMessageConsumer, NotificationConsumer, 
                                    NotificationTypeConsumer)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GossipBooks.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path("room/<username>/", ChatMessageConsumer.as_asgi(), name="Chat-Consumer-URL"),
                    path("notification/", NotificationConsumer.as_asgi(), ),
                ]
            )
        )
    )
})
