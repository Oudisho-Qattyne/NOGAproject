from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/source/", consumers.SourceConsumer.as_asgi()),
    path("ws/view/", consumers.ViewerConsumer.as_asgi()),
]