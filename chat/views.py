from django.shortcuts import render

def chat_page(request):
    return render(request, "chat.html")

def voice_chat(request):
    return render(request, "chat.html")