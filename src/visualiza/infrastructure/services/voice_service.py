import speech_recognition as sr
import pyttsx3

class VoiceService:
    """
    Handles Speech-to-Text (STT) and Text-to-Speech (TTS) functionalities.
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()

        # Optional: Configure voice, rate, etc.
        # self.tts_engine.setProperty('voice', 'your_voice_id')
        # self.tts_engine.setProperty('rate', 150)

    def speak(self, text: str):
        """
        Converts text to speech and speaks it out loud.
        """
        print(f"TTS: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen_and_transcribe(self) -> str | None:
        """
        Listens for audio via the microphone and transcribes it to text using Sphinx.
        Returns the transcribed text or None if it fails.
        """
        with sr.Microphone() as source:
            print("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("DEBUG: No speech detected within the timeout.")
                return None

        try:
            print("Reconociendo...")
            # Using Sphinx for offline recognition
            text = self.recognizer.recognize_sphinx(audio, language="es-ES")
            print(f"STT: Detected text: '{text}'")
            return text.lower()
        except sr.UnknownValueError:
            self.speak("Lo siento, no he podido entenderte.")
            return None
        except sr.RequestError as e:
            # This is for online recognizers, but good practice to keep
            self.speak("Error de conexión. No se pudo contactar al servicio de reconocimiento.")
            print(f"Sphinx error: {e}")
            return None
