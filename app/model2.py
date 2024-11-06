import speech_recognition as sr
import os
from google.cloud import speech


# Reemplaza con tu clave de API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'AIzaSyA2-bpfUVrdJYtDR26t1dEqv1nE9FNDRxQ'

client = speech.SpeechClient()

def escuchar():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("escuchando... ")
            voice = listener.listen(source)
            rec = listener.recognize_google_cloud(voice)
            print(rec)

    except:
        pass


if __name__ == "__main__":
    escuchar()