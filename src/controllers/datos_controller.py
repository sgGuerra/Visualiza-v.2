from src.models.datos_usuario_model import DatosUsuarioModel
from src.controllers.asistente_controller import AsistenteController
from src.utils.errores import EdadInvalidaError

class DatosUsuarioController:
    def __init__(self):
        self.model = DatosUsuarioModel()
        self.asistente = AsistenteController()

    def solicitar_dato(self, mensaje: str) -> str:
        self.asistente.hablar(mensaje)
        return self.asistente.obtener_respuesta()

    def solicitar_datos_usuario(self):
        # Solicitar nombre
        nombre = self.solicitar_dato("Por favor, dime como quieres que te llame:")
        
        # Solicitar género
        genero = self.solicitar_dato("Ahora dime cuál es tu género:")
        
        # Solicitar edad
        edad = None
        while edad is None:
            try:
                edad_texto = self.solicitar_dato("Ahora dime tu edad, solo el número sin decir años.")
                edad_numero = self.model.convertir_texto_a_numero(edad_texto)
                if edad_numero and self.model.validar_edad(edad_numero):
                    edad = edad_numero
                else:
                    raise EdadInvalidaError(edad_texto, "La edad ingresada no es válida.")
            except EdadInvalidaError as e:
                self.asistente.hablar(str(e))
                self.asistente.hablar("Por favor, intenta de nuevo.")

        # Solicitar estado civil
        estado_civil = self.solicitar_dato("Por favor, dime tu estado civil:")
        
        # Crear persona con los datos recolectados
        self.model.crear_persona(nombre, edad, genero, estado_civil)

    def mostrar_datos_guardados(self):
        datos = self.model.obtener_datos_persona()
        if datos:
            self.asistente.hablar("Los datos ingresados son los siguientes:")
            for clave, valor in datos.items():
                mensaje = f"{clave}: {valor}"
                print(mensaje)
                self.asistente.hablar(mensaje)
