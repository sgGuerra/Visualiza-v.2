from app.model import AsistenteVisualiza
from complementos.errores import EdadInvalidaError


class SolicitudDatos:
    def __init__(self):
        self.interaccion = AsistenteVisualiza()
        self.datos_usuario = {}  # Diccionario para almacenar los datos del usuario

    def texto_a_numero(self, texto):
        numeros = {
            "cero": 0,
            "uno": 1,
            "dos": 2,
            "tres": 3,
            "cuatro": 4,
            "cinco": 5,
            "seis": 6,
            "siete": 7,
            "ocho": 8,
            "nueve": 9,
            "diez": 10,
            "once": 11,
            "doce": 12,
            "trece": 13,
            "catorce": 14,
            "quince": 15,
            "dieciséis": 16,
            "diecisiete": 17,
            "dieciocho": 18,
            "diecinueve": 19,
            "veinte": 20,
            "treinta": 30,
            "cuarenta": 40,
            "cincuenta": 50,
            "sesenta": 60,
            "setenta": 70,
            "ochenta": 80,
            "noventa": 90,
            "cien": 100
        }

        texto = texto.lower().strip()
        if texto in numeros:
            return numeros[texto]
        else:
            # Manejo de números compuestos (ejemplo: veintiuno, treinta y dos)
            partes = texto.split(" y ")
            numero = 0
            for parte in partes:
                if parte in numeros:
                    numero += numeros[parte]
                elif parte.startswith("veinti"):
                    unidad = parte.replace("veinti", "")
                    numero += 20 + numeros.get(unidad, 0)
                else:
                    return None  # Número no reconocido
            return numero

    # Función para solicitar un dato ya sea por voz o manualmente
    def solicitar_dato(self, mensaje):
        self.interaccion.hablar(mensaje)
        print(mensaje)
        dato = self.interaccion.reconocer_audio(self.interaccion.escuchar_voz())
        if not dato:
            self.interaccion.hablar("No se entendió. Por favor, ingrese los datos manualmente.")
            dato = input("Ingrese los datos manualmente: ")
        return dato

    # Función para validar que la edad sea correcta (un número válido)
    def validar_edad(self, edad):
        if 0 < edad < 120:
            return edad
        else:
            raise EdadInvalidaError(edad, "La entrada no es un número válido.")

    # Función principal para solicitar todos los datos del usuario
    def solicitar_datos_usuario(self):
        # Solicitar nombre completo
        nombre = self.solicitar_dato("Por favor, dime como quieres que te llame:")
        self.datos_usuario["Nombre"] = nombre

        genero = self.solicitar_dato("ahora dime cual es tu genero: ")
        self.datos_usuario["Genero"] = genero

        # Solicitar edad
        while True:
            try:
                edad = self.solicitar_dato("Ahora dime tu edad, solo el número sin decir años.")
                edad_numero = self.texto_a_numero(edad)
                print(edad_numero)
                edad_validada = self.validar_edad(edad_numero)
                if edad_validada is not None:
                    self.datos_usuario["Edad"] = edad_validada
                    break
                else:
                    raise EdadInvalidaError(edad_numero, "La edad ingresada no es válida. Por favor, ingrese manualmente.")
            except EdadInvalidaError as e:
                self.interaccion.hablar(e.mensaje)
                print(e.mensaje)
                try:
                    self.interaccion.hablar("Se ha habilitado el ingreso de edad de forma manúal.")
                    edad_manual = int(input("ingrese la edad manualmente: "))
                    edad_validada = self.validar_edad(edad_manual)
                    if edad_validada is not None:
                        self.datos_usuario["Edad"] = edad_validada
                        break
                except ValueError:
                    self.interaccion.hablar("Por favor, ingrese un número válido.")

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
