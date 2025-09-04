import whisper
import os
import warnings
from pydub import AudioSegment

class Transcriber:
    def __init__(self):
        # Cargar el modelo de Whisper (se descargará la primera vez)
        print("Cargando modelo de Whisper...")
        # Suprimir la advertencia de FP16 y forzar FP32 para CPU
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
        self.model = whisper.load_model("medium", device="cpu")
        print("Modelo de Whisper cargado!")
        
    def transcribe(self, audio):
        try:
            print("\n=== Iniciando transcripción con Whisper ===")

            # Guardar el audio temporalmente
            temp_path = "temp_audio"
            audio.save(temp_path)
            print("Audio guardado temporalmente")

            # Cargar y convertir a 16kHz mono WAV
            print("Convirtiendo audio a 16kHz mono WAV...")
            sound = AudioSegment.from_file(temp_path)
            sound = sound.set_channels(1).set_frame_rate(16000)
            sound.export("audio.wav", format="wav")
            print("Audio convertido y guardado como audio.wav")

            # Eliminar archivo temporal
            if os.path.exists(temp_path):
                os.remove(temp_path)

            # Realizar la transcripción
            print("Transcribiendo audio...")
            result = self.model.transcribe("audio.wav")

            # Mostrar detalles de la transcripción
            text = result["text"].strip()
            print("\nResultado de la transcripción:")
            print("-------------------------------")
            print(f"Texto detectado: {text}")
            if 'segments' in result:
                print("\nSegmentos detectados:")
                for segment in result['segments']:
                    print(f"- Tiempo: {segment['start']:.1f}s - {segment['end']:.1f}s")
                    print(f"  Texto: {segment['text']}")
                    if 'confidence' in segment:
                        print(f"  Confianza: {segment['confidence']:.2%}")
            print("-------------------------------")

            # Eliminar el archivo WAV temporal
            if os.path.exists("audio.wav"):
                os.remove("audio.wav")
                print("Archivo de audio temporal eliminado")

            return text

        except Exception as e:
            print(f"\n❌ Error en la transcripción local: {str(e)}")
            # Limpiar archivos temporales en caso de error
            for temp_file in ["temp_audio", "audio.wav"]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    print(f"Archivo temporal {temp_file} eliminado después del error")
            raise e
