import whisper
import os

class Transcriber:
    def __init__(self):
        # Cargar el modelo de Whisper (se descargará la primera vez)
        print("Cargando modelo de Whisper...")
        self.model = whisper.load_model("medium")
        print("Modelo de Whisper cargado!")
        
    # Siempre guarda y lee del archivo audio.mp3
    def transcribe(self, audio):
        try:
            print("\n=== Iniciando transcripción con Whisper ===")
            
            # Guardar el audio
            audio.save("audio.mp3")
            print("Audio guardado temporalmente como audio.mp3")
            
            # Realizar la transcripción
            print("Transcribiendo audio...")
            result = self.model.transcribe("audio.mp3")
            
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
            
            # Eliminar el archivo temporal
            if os.path.exists("audio.mp3"):
                os.remove("audio.mp3")
                print("Archivo de audio temporal eliminado")
                
            return text
            
        except Exception as e:
            print(f"\n❌ Error en la transcripción local: {str(e)}")
            if os.path.exists("audio.mp3"):
                os.remove("audio.mp3")
                print("Archivo de audio temporal eliminado después del error")
            raise e