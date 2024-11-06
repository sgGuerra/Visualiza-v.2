import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import pyttsx3
import warnings

temp_file = tempfile.mkdtemp()
save_path = os.path.join(temp_file, 'temp.wav')


# Clase para manejar la interacción de voz y texto
class AsistenteVisualiza:
    def __init__(self):
        self.listener = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.voz_asistente = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'
        self.cambiar_voz(self.voz_asistente)
        self.velocidad_voz(160)


    def cambiar_voz(self, voice_id):
        for voice in self.voices:
            if voice.id == voice_id:
                self.engine.setProperty('voice', voice.id)
                break

    def velocidad_voz(self, rate):
        self.engine.setProperty('rate', rate)

    # Función para hablar al usuario
    def hablar(self, texto):
        self.engine.say(texto)
        self.engine.runAndWait()

    # Función para obtener entrada de voz
    def escuchar_voz(self):
        try:
            with sr.Microphone() as source:
                print("Escuchando...")
                self.listener.adjust_for_ambient_noise(source)
                audio = self.listener.listen(source)
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)
                audio_clip.export(save_path, format='wav')

        except sr.UnknownValueError:
            print("No entendí lo que dijiste.")
            return None

        return save_path

    # Función para reconocer y transcribir audio
    def reconocer_audio(self, save_path):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            try:
                audio_model = whisper.load_model('small', )
                transcription = audio_model.transcribe(save_path, language="spanish", fp16=False)
                return transcription['text']

            except Exception as e:
                print(f"Ocurrió un error al reconocer el audio: {e}")
                return None

    # Nueva función para obtener la respuesta del usuario
    def obtener_respuesta(self):
        ruta_audio = self.escuchar_voz()
        if ruta_audio:
            texto = self.reconocer_audio(ruta_audio)
            if texto:
                print(f"Usuario dijo: {texto}")
                return texto
            else:
                self.hablar("No pude entender tu respuesta. Por favor, intenta de nuevo.")
                return self.obtener_respuesta()
        else:
            self.hablar("No recibí ninguna respuesta. Por favor, intenta de nuevo.")
            return self.obtener_respuesta()
