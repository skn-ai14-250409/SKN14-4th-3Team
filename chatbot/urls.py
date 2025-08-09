from django.urls import path
from .views import ChatBotView, ModelSearchView, ConversationView, MessageView, ConversationDetailView

urlpatterns = [
    path("chat/", ChatBotView.as_view(), name="chat"),
    path("model-search/", ModelSearchView.as_view(), name="model-search"),
    path("audio-chat/", AudioChatView.as_view(), name="audio_chat"),
    path("tts/", TTSView.as_view(), name="tts"),
    path("conversations/", ConversationView.as_view(), name="conversations"),
    path("conversations/<int:conversation_id>/", ConversationDetailView.as_view(), name="conversation-detail"),
    path("conversations/<int:conversation_id>/messages/", MessageView.as_view(), name="messages"),
]
