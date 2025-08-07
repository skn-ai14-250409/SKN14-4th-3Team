from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat'),
    path("voicechat/", views.voice_chat, name="voice_chat"),
    path("", views.chat_view, name="chat"),  # chat.html을 렌더링하는 view
    path('api/audio-chat/', views.audio_chat),
    path('api/chat/', views.chat),
    path('api/tts/', views.tts),
]
