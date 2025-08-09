import base64
import tempfile
import os
from openai import OpenAI
import openai
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skn4th.settings")

from django.conf import settings 
openai.api_key = settings.OPENAI_API_KEY
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def stt(mp3_bytes):
    # bytes -> 파일 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
        f.write(mp3_bytes)
        f.flush()
        fname = f.name

    with open(fname, 'rb') as f:
        transcription = client.audio.transcriptions.create(
            model='whisper-1',
            file=f
        )
    os.remove(fname)
    return transcription.text

def ask_gpt(messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        top_p=1,
        max_tokens=4096
    )
    return response.choices[0].message.content

def tts(text):
    fname = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
    with client.audio.speech.with_streaming_response.create(
        model='tts-1',
        voice='alloy',
        input=text
    ) as stream:
        stream.stream_to_file(fname)
    with open(fname, 'rb') as f:
        data = f.read()
        base64_encoded = base64.b64encode(data).decode()
    os.remove(fname)
    return base64_encoded
