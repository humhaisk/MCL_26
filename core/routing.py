from django.urls import path
from core import consumers


websocket_urlpatterns = [
    # Define your WebSocket URL patterns here
    # re_path("ws/ac/", consumers.MyConsumer.as_asgi()),
    path("ws/ac/", consumers.MyConsumer.as_asgi()),  
]