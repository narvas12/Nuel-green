# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from .consumer import CodeExecutionConsumer
from django.urls import path

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        [
            # Add WebSocket consumers here
            path("ws/code_execution/", CodeExecutionConsumer.as_asgi()),

        ]
    ),
})
