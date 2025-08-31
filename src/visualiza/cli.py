# A command-line interface for end-to-end testing without a GUI.
import sys
import os
import numpy as np
import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.visualiza.application.services.user_service import UserApplicationService
from src.visualiza.infrastructure.persistence.sqlite_repository import SQLiteUserRepository
from src.visualiza.infrastructure.services.voice_service import VoiceService
from src.visualiza.infrastructure.services.vision_service import VisionService

def run_cli():
    """
    Runs a command-line smoke test of the application's services.
    """
    print("--- Initializing Services for CLI Test ---")
    user_repository = SQLiteUserRepository()
    user_service = UserApplicationService(user_repository)
    voice_service = VoiceService()
    vision_service = VisionService(model_path="yolov8n.pt")

    print("\n--- Testing User Registration ---")
    voice_service.speak("Bienvenido al test de Visualiza. Vamos a registrar un usuario.")

    try:
        user = user_service.register_user("CLI User", 25, "Non-binary", "Testing")
        print(f"Usuario registrado: {user.name}")
        voice_service.speak(f"Usuario {user.name} registrado correctamente.")
    except Exception as e:
        print(f"Error en el registro: {e}")
        return

    retrieved_user = user_service.get_user()
    if retrieved_user:
        print(f"Usuario obtenido: {retrieved_user.name}")
    else:
        print("Error: No se pudo obtener el usuario.")
        return

    print("\n--- Testing Vision Service (simulated) ---")
    voice_service.speak("Ahora, probaremos el servicio de visión con una imagen de prueba.")

    # Create a dummy black image for testing purposes
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    try:
        annotated_frame, detected_objects = vision_service.detect_objects(dummy_frame)
        print(f"Servicio de visión ejecutado. Objetos detectados: {detected_objects}")

        if detected_objects:
            voice_service.speak(f"En la imagen de prueba veo: {', '.join(detected_objects)}")
        else:
            voice_service.speak("No se detectaron objetos en la imagen de prueba.")

        # To prove it worked, we can check the output frame size
        assert annotated_frame.shape == dummy_frame.shape
        print("La imagen anotada tiene las dimensiones correctas.")

    except Exception as e:
        print(f"Error en la detección de objetos: {e}")
        return

    print("\n--- CLI Test Complete ---")

if __name__ == "__main__":
    run_cli()
