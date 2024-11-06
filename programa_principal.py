from app.model import AsistenteVisualiza
from app.datos_usuario import SolicitudDatos
from app.persona import Persona
from app.reconocer_objetos import DetectorObjetos
from complementos.errores import RespuestaInvalidaError
from interfaz import InterfazVisualiza

class ProgramaPrincipal:
    def __init__(self):
        self.solicitud = SolicitudDatos()
        self.detector = DetectorObjetos()
        self.asistente = AsistenteVisualiza()

    def ejecutar_programa(self, ):
        self.asistente.hablar("Bienvenido me llamo Visualiza.")
        self.asistente.hablar("Vamos a registrar tus datos para comenzar.")

        datos_validos = False
        while not datos_validos:
            self.solicitud.solicitar_datos_usuario()
            self.solicitud.mostrar_datos_guardados()

            # Preguntar al usuario si los datos son correctos
            self.asistente.hablar("¿Los datos son correctos? Por favor responde con 'correctos' o 'incorrectos'.")
            respuesta = self.asistente.obtener_respuesta().strip().lower()

            if "correctos" in respuesta:
                datos_validos = True
            elif "incorrectos" in respuesta:
                self.asistente.hablar("Vamos a reingresar tus datos.")

        try:
            self.asistente.hablar("¿Deseas iniciar la detección de objetos? Responde uno para 'sí' o dos para'no'.")
            respuesta = self.asistente.obtener_respuesta().strip().lower()

            if respuesta not in ["uno", "dos"]:
                raise RespuestaInvalidaError(respuesta)

            if "uno" in respuesta:
                self.detector.iniciar_deteccion()
            elif "dos" in respuesta:
                self.asistente.hablar("Gracias por usar Visualiza. ¡Hasta pronto!")
                exit()

        except RespuestaInvalidaError as e:
            self.asistente.hablar(e.mensaje)
            respuesta_manual = input("Por favor, ingrese '1' para sí o '2' para no: ")

            if respuesta_manual == "1":
                self.detector.iniciar_deteccion()
            elif respuesta_manual == "2":
                self.asistente.hablar("Gracias por usar Visualiza. ¡Hasta pronto!")
                exit()



if __name__ == "__main__":
    app = InterfazVisualiza()
    app.iniciar()