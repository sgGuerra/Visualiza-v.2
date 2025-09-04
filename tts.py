import os
from dotenv import load_dotenv
import requests

#Texto a voz. Esta impl utiliza ElevenLabs
class TTS():
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('ELEVENLABS_API_KEY')
    
    def process(self, text):
        CHUNK_SIZE = 1024
        # Utiliza la voz especifica de Bella
        url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.key
        }

        data = {
            "text": text,
            "model_id": "eleven_multilingual_v1",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.55
            }
        }

        # Genera un nombre único para cada respuesta usando timestamp
        import time
        file_name = f"response_{int(time.time())}.mp3"
        
        # Eliminar archivos antiguos de respuesta
        import os
        for file in os.listdir("static"):
            if file.startswith("response_") and file.endswith(".mp3"):
                try:
                    os.remove(os.path.join("static", file))
                except:
                    pass

        # Guardar nueva respuesta
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open("static/" + file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            return file_name
        else:
            print(f"Error en ElevenLabs API: {response.status_code}")
            return None