import cv2
from src.models.detector_model import DetectorModel
from src.controllers.asistente_controller import AsistenteController

class DetectorController:
    def __init__(self):
        self.model = DetectorModel()
        self.asistente = AsistenteController()

    def iniciar_deteccion(self):
        if not self.model.inicializar_camara():
            self.asistente.hablar("No se pudo inicializar la cámara.")
            return

        self.asistente.hablar("Iniciando detección de objetos. Presiona Q para salir.")

        while True:
            success, frame = self.model.obtener_frame()
            if not success:
                break

            # Realizar la detección
            frame_anotado, objetos = self.model.detectar_objetos(frame)

            # Anunciar objetos detectados
            if objetos:
                mensaje = f"Detectado: {', '.join(objetos)}"
                print(mensaje)
                self.asistente.hablar(mensaje)

            # Mostrar el frame con las detecciones
            cv2.imshow("Detección de Objetos", frame_anotado)

            # Salir si se presiona 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.model.liberar_recursos()
