#pip install django channels daphne openai channels_redis pydub soundfile
import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .openai_service import stt, ask_gpt, tts
from django.conf import settings
import aiohttp

class VoiceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.messages = [{'role':'system', 'content':'당신은 친절한 챗봇입니다.'}]

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
    # 1. 음성 데이터(STT)
        if bytes_data:
            # OpenAI Whisper API 호출 (비동기)
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
                data = aiohttp.FormData()
                data.add_field('file', bytes_data, filename='audio.mp3', content_type='audio/mp3')
                data.add_field('model', 'whisper-1')
                async with session.post("https://api.openai.com/v1/audio/transcriptions", headers=headers, data=data) as resp:
                    stt_result = await resp.json()
            prompt = stt_result.get("text", "")

            # 2. GPT 챗봇 (예시: 기존 함수 사용)
            # 실제 챗봇 함수에 맞게 수정 필요
            from chatbot.rag_engine import run_chatbot
            response = run_chatbot(prompt)

            # 3. TTS (OpenAI TTS)
            async with session.post(
                "https://api.openai.com/v1/audio/speech",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "tts-1",
                    "input": response,
                    "voice": "nova"
                }
            ) as tts_resp:
                tts_audio = await tts_resp.read()
            audio_base64 = base64.b64encode(tts_audio).decode("utf-8")

            # 4. 결과 전송
            await self.send(text_data=json.dumps({
                "prompt": prompt,
                "response": response,
                "audio_base64": audio_base64
            }))




# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data["message"]
#         # 클라이언트에 메시지 그대로 다시 전송
#         await self.send(text_data=json.dumps({"message": message}))            