from ultralytics import YOLO
import cv2
import numpy as np

class DetectorModel:
    def __init__(self):
        self.modelo = YOLO('yolov8n.pt')
        self.cap = None

    def inicializar_camara(self):
        self.cap = cv2.VideoCapture(0)
        return self.cap.isOpened()

    def obtener_frame(self):
        if self.cap and self.cap.isOpened():
            return self.cap.read()
        return False, None

    def detectar_objetos(self, frame):
        resultados = self.modelo(frame)
        objetos_detectados = []
        
        for r in resultados:
            anotaciones = r.plot()
            for box in r.boxes:
                clase = r.names[int(box.cls[0])]
                confianza = float(box.conf[0])
                if confianza > 0.5 and clase not in objetos_detectados:
                    objetos_detectados.append(clase)
            
            return anotaciones, objetos_detectados

        return frame, []

    def liberar_recursos(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
