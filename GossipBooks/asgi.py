from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.urls import path
import os
from channels.routing import get_default_application
import django
from messaging.consumers import ChatMessageConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GossipBooks.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

application = ProtocolTypeRouter({
    # "http": get_default_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                   path("room/<username>/", ChatMessageConsumer.as_asgi(), name="Chat-Consumer-URL"),
                ]
            )
        )
    )
})
