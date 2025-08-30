from src.controllers.asistente_controller import AsistenteController
from src.controllers.datos_controller import DatosUsuarioController
from src.controllers.detector_controller import DetectorController
from src.utils.errores import RespuestaInvalidaError

class InterfazView:
    def __init__(self):
        self.asistente = AsistenteController()
        self.datos_controller = DatosUsuarioController()
        self.detector = DetectorController()

    def mostrar_bienvenida(self):
        self.asistente.hablar("Bienvenido me llamo Visualiza.")
        self.asistente.hablar("Vamos a registrar tus datos para comenzar.")

    def solicitar_confirmacion_datos(self):
        datos_validos = False
        while not datos_validos:
            self.datos_controller.solicitar_datos_usuario()
            self.datos_controller.mostrar_datos_guardados()

            self.asistente.hablar("¿Los datos son correctos? Por favor responde con 'correctos' o 'incorrectos'.")
            respuesta = self.asistente.obtener_respuesta().strip().lower()

            if "correctos" in respuesta:
                datos_validos = True
            elif "incorrectos" in respuesta:
                self.asistente.hablar("Vamos a reingresar tus datos.")

    def solicitar_inicio_deteccion(self):
        try:
            self.asistente.hablar("¿Deseas iniciar la detección de objetos? Responde 'uno' para sí o 'dos' para no.")
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

    def iniciar(self):
        self.mostrar_bienvenida()
        self.solicitar_confirmacion_datos()
        self.solicitar_inicio_deteccion()
