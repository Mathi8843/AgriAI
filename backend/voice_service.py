import speech_recognition as sr
from gtts import gTTS
import os
import uuid

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio file to text using Google Speech Recognition.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"STT Error: {e}")
        return ""

def text_to_speech(text: str, output_dir: str = "static") -> str:
    """
    Convert text to speech and save as MP3. Returns the filename.
    """
    try:
        if not text:
            text = "I did not understand that."
            
        tts = gTTS(text=text, lang='en')
        filename = f"response_{uuid.uuid4().hex[:8]}.mp3"
        file_path = os.path.join(output_dir, filename)
        tts.save(file_path)
        return filename
    except Exception as e:
        print(f"TTS Error: {e}")
        return ""
