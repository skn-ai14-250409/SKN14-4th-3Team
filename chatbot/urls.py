from django.urls import path
from .views import ChatBotView, ModelSearchView, AudioChatView, TTSView


urlpatterns = [
    path("chat/", ChatBotView.as_view(), name="chat"),
    path("model-search/", ModelSearchView.as_view(), name="model-search"),
    path("audio-chat/", AudioChatView.as_view(), name="audio_chat"),
    path("tts/", TTSView.as_view(), name="tts"),

]
