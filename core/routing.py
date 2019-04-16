# chat/routing.py
from django.conf.urls import url

from core import Consumer

websocket_urlpatterns = [
    url(r'^ws/core/(?P<room_name>[^/]+)/$', Consumer.TaskConsumer),
]