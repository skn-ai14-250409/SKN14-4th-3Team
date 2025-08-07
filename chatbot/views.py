import os
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import requests
from dotenv import load_dotenv 
from django.conf import settings

from .rag_engine import run_chatbot, search_vector_db_image

openai_api_key = settings.OPENAI_API_KEY

@method_decorator(csrf_exempt, name="dispatch")
class ChatBotView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            query = body.get("query", "")
            history = body.get("history", [])

            result = run_chatbot(query, history=history)
            return JsonResponse({"response": result})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class ModelSearchView(View):
    def post(self, request):
        image_file = request.FILES.get("image")
        if not image_file:
            return HttpResponseBadRequest("No image file uploaded.")

        # 임시 저장
        temp_path = f"/tmp/{image_file.name}"
        with open(temp_path, "wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        try:
            model_code = search_vector_db_image(temp_path)
            return JsonResponse({"model_code": model_code})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class AudioChatView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        audio_file = request.FILES.get("file")
        if not audio_file:
            return HttpResponseBadRequest("No audio file uploaded.")

        # OpenAI Whisper API 호출 
        openai_api_key = "OPENAI_API_KEY"
        stt_res = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {openai_api_key}"},
            files={"file": (audio_file.name, audio_file, audio_file.content_type)},
            data={"model": "whisper-1"}
        )
        stt_data = stt_res.json()
        recognized_text = stt_data.get("text", "")

        return JsonResponse({"text": recognized_text})

class TTSView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        body = json.loads(request.body)
        text = body.get("text", "")
        if not text:
            return HttpResponseBadRequest("No text provided.")

        # OpenAI TTS API 호출 
        openai_api_key = "OPENAI_API_KEY"
        tts_res = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "tts-1",
                "input": text,
                "voice": "nova"
            }
        )
        return HttpResponse(tts_res.content, content_type="audio/wav")