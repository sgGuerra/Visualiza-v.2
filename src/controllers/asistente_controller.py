from src.models.asistente_model import AsistenteModel

class AsistenteController:
    def __init__(self):
        self.model = AsistenteModel()
        self.model.set_voice(self.model.voz_asistente)
        self.model.set_rate(160)

    def hablar(self, texto):
        self.model.engine.say(texto)
        self.model.engine.runAndWait()

    def obtener_respuesta(self):
        ruta_audio = self.model.get_audio_data()
        if ruta_audio:
            texto = self.model.transcribe_audio(ruta_audio)
            if texto:
                print(f"Usuario dijo: {texto}")
                return texto
            else:
                self.hablar("No pude entender tu respuesta. Por favor, intenta de nuevo.")
                return self.obtener_respuesta()
        else:
            self.hablar("No recibí ninguna respuesta. Por favor, intenta de nuevo.")
            return self.obtener_respuesta()
