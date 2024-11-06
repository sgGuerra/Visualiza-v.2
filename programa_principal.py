from app.model import AsistenteVisualiza
from app.datos_usuario import SolicitudDatos

class ProgramaPrincipal:
    def ejecutar_programa(self):
        asistente = AsistenteVisualiza()
        response = asistente.reconocer_audio(asistente.escuchar_voz())
        asistente.hablar(response)
        print(response)


# Ejecutar el programa
if __name__ == "__main__":
    programa = ProgramaPrincipal()
    programa.ejecutar_programa()