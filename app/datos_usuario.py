from app.model import AsistenteVisualiza


class SolicitudDatos:
    def __init__(self):
        self.interaccion = AsistenteVisualiza()
        self.datos_usuario = {}  # Diccionario para almacenar los datos del usuario

    # Función para solicitar un dato ya sea por voz o manualmente
    def solicitar_dato(self, mensaje):
        self.interaccion.hablar(mensaje)
        print(mensaje)
        dato = self.interaccion.escuchar_voz()
        if dato is None:
            self.interaccion.hablar("No se entendió. Por favor, ingrese los datos manualmente.")
            dato = input("Ingrese los datos manualmente: ")
        return dato

    # Función para validar que la edad sea correcta (un número válido)
    def validar_edad(self, edad_texto):
        try:
            edad = int(edad_texto)
            if 0 <= edad <= 120:  # Validamos que la edad esté en un rango razonable
                return edad
            else:
                return None
        except ValueError:
            return None

    # Función principal para solicitar todos los datos del usuario
    def solicitar_datos_usuario(self):
        # Solicitar nombre completo
        nombre = self.solicitar_dato("Por favor, diga su nombre completo:")
        self.datos_usuario["Nombre"] = nombre

        # Solicitar la edad y validarla
        while True:
            edad = self.solicitar_dato("Diga su edad:")
            edad_validada = self.validar_edad(edad)
            if edad_validada is not None:
                self.datos_usuario["Edad"] = edad_validada
                break
            else:
                self.interaccion.hablar("Edad inválida. Por favor, inténtelo de nuevo.")
                print("Edad inválida. Por favor, inténtelo de nuevo.")

        # Solicitar estado civil
        estado_civil = self.solicitar_dato("Por favor, diga su estado civil:")
        self.datos_usuario["Estado civil"] = estado_civil

    # Función para mostrar los datos del usuario guardados
    def mostrar_datos_guardados(self):
        self.interaccion.hablar("Los datos ingresados son los siguientes:")
        print("\n--- Datos del Usuario ---")
        for clave, valor in self.datos_usuario.items():
            print(f"{clave}: {valor}")
            self.interaccion.hablar(f"{clave}: {valor}")