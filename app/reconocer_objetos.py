from ultralytics import YOLO
import cv2
import numpy as np
from app.model import AsistenteVisualiza


class DetectorObjetos:
    def __init__(self):
        self.modelo = YOLO('yolov8n.pt')  # Usando el modelo más ligero de YOLOv8
        self.asistente = AsistenteVisualiza()

    def iniciar_deteccion(self):
        # Inicializar la webcam
        cap = cv2.VideoCapture(0)

        self.asistente.hablar("Iniciando detección de objetos. Presiona Q para salir.")

        while cap.isOpened():
            success, frame = cap.read()

            if success:
                # Realizar la detección
                resultados = self.modelo(frame)

                # Procesar los resultados
                for r in resultados:
                    anotaciones = r.plot()  # Dibuja las cajas y etiquetas

                    # Obtener y anunciar los objetos detectados
                    objetos_detectados = []
                    for box in r.boxes:
                        clase = r.names[int(box.cls[0])]
                        confianza = float(box.conf[0])
                        if confianza > 0.5 and clase not in objetos_detectados:  # Solo anunciar si confianza > 50%
                            objetos_detectados.append(clase)

                    if objetos_detectados:
                        mensaje = f"Detectado: {', '.join(objetos_detectados)}"
                        print(mensaje)
                        self.asistente.hablar(mensaje)

                    # Mostrar el frame con las detecciones
                    cv2.imshow("Detección de Objetos", anotaciones)

                # Salir si se presiona 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

