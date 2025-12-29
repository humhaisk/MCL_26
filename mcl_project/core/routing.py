from django.urls import re_path
from core import consumers

websocket_urlpatterns = [
    re_path("ws/ac/", consumers.MyConsumer.as_asgi()), 
]