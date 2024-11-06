from app.model import AsistenteVisualiza
from app.datos_usuario import SolicitudDatos
from app.persona import Persona


class ProgramaPrincipal:
    def __init__(self):
        self.solicitud = SolicitudDatos()

    def ejecutar_programa(self):
        asistente = AsistenteVisualiza()
        asistente.hablar("Bienvenido me llamo Visualiza.")
        asistente.hablar("Vamos a registrar tus datos para comenzar.")

        datos_validos = False
        while not datos_validos:
            self.solicitud.solicitar_datos_usuario()
            self.solicitud.mostrar_datos_guardados()

            # Preguntar al usuario si los datos son correctos
            asistente.hablar("¿Los datos son correctos? Por favor responde con 'correctos' o 'incorrectos'.")
            respuesta = asistente.obtener_respuesta().strip().lower()

            if "correctos" in respuesta:
                datos_validos = True
            elif "incorrectos" in respuesta:
                asistente.hablar("Vamos a reingresar tus datos.")


# Ejecutar el programa
if __name__ == "__main__":
    programa = ProgramaPrincipal()
    programa.ejecutar_programa()
