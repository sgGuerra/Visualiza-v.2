import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import json
from transcriber import Transcriber
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand

#Cargar llaves del archivo .env
load_dotenv()
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    print("\n=== Nueva solicitud de audio recibida ===")
    
    # Obtener audio grabado y transcribirlo
    audio = request.files.get("audio")
    print("Audio recibido, iniciando transcripción...")
    
    text = Transcriber().transcribe(audio)
    print("\n=== Transcripción completada ===")
    print(f"Texto a procesar: '{text}'")
    
    # Utilizar el LLM para ver si llamar una funcion
    print("\nProcesando texto con el modelo de lenguaje...")
    llm = LLM()
    function_name, args, message = llm.process_functions(text)
    if function_name is not None:
        #Si se desea llamar una funcion de las que tenemos
        if function_name == "get_weather":
            #Llamar a la funcion del clima
            function_response = Weather().get(args["ubicacion"])
            function_response = json.dumps(function_response)
            print(f"Respuesta de la funcion: {function_response}")
            
            final_response = llm.process_response(text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "send_email":
            #Llamar a la funcion para enviar un correo
            final_response = "Esta función aún no está implementada."
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "open_chrome":
            PcCommand().open_chrome(args["website"])
            final_response = "Listo, ya abrí chrome en el sitio " + args["website"]
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "dominate_human_race":
            final_response = "No te creas. Suscríbete al canal!"
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
    else:
        final_response = "Disculpa, no he entendido bien tu solicitud. ¿Podrías repetirla de forma más clara y pausada? Estoy aquí para ayudarte con información del clima, enviar correos, abrir sitios web o asistirte en otras tareas."
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}