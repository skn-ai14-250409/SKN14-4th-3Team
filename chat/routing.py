from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    #path('ws/voicechat/', consumers.VoiceChatConsumer.as_asgi()),
    #re_path(r"ws/chat/$", consumers.ChatConsumer.as_asgi()),
#
    re_path(r"ws/voicechat/$", consumers.VoiceChatConsumer.as_asgi()),
]

