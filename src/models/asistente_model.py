import io
import os
import tempfile
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import pyttsx3
import warnings

class AsistenteModel:
    def __init__(self):
        self.listener = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.voz_asistente = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'
        self.temp_dir = tempfile.mkdtemp()
        self.save_path = os.path.join(self.temp_dir, 'temp.wav')

    def set_voice(self, voice_id):
        for voice in self.voices:
            if voice.id == voice_id:
                self.engine.setProperty('voice', voice.id)
                break

    def set_rate(self, rate):
        self.engine.setProperty('rate', rate)

    def get_audio_data(self):
        try:
            with sr.Microphone() as source:
                print("Escuchando...")
                self.listener.adjust_for_ambient_noise(source)
                audio = self.listener.listen(source)
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)
                audio_clip.export(self.save_path, format='wav')
                return self.save_path
        except sr.UnknownValueError:
            return None

    def transcribe_audio(self, audio_path):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            try:
                audio_model = whisper.load_model('small')
                transcription = audio_model.transcribe(audio_path, language="spanish", fp16=False)
                return transcription['text']
            except Exception as e:
                print(f"Error al reconocer el audio: {e}")
                return None
