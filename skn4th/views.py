def my_stt(audio_file):
    
    import openai
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

def my_gpt(query, history):
    
    import openai
    messages = [{"role": h['role'], "content": h['content']} for h in history]
    messages.append({"role": "user", "content": query})
    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages
    )
    return resp.choices[0].message['content']

def my_tts(text):
    from gtts import gTTS
    import io
    tts = gTTS(text=text, lang='ko')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    return fp.getvalue()
