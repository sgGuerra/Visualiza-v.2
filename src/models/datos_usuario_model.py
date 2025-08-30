from src.models.persona_model import PersonaModel
from src.utils.errores import EdadInvalidaError

class DatosUsuarioModel:
    def __init__(self):
        self.numeros = {
            "cero": 0, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4,
            "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
            "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14,
            "quince": 15, "dieciséis": 16, "diecisiete": 17, "dieciocho": 18,
            "diecinueve": 19, "veinte": 20, "treinta": 30, "cuarenta": 40,
            "cincuenta": 50, "sesenta": 60, "setenta": 70, "ochenta": 80,
            "noventa": 90, "cien": 100
        }
        self.persona = None

    def convertir_texto_a_numero(self, texto: str) -> int:
        texto = texto.lower().strip()
        if texto in self.numeros:
            return self.numeros[texto]
        
        partes = texto.split(" y ")
        numero = 0
        for parte in partes:
            if parte in self.numeros:
                numero += self.numeros[parte]
            elif parte.startswith("veinti"):
                unidad = parte.replace("veinti", "")
                numero += 20 + self.numeros.get(unidad, 0)
            else:
                return None
        return numero

    def validar_edad(self, edad: int) -> bool:
        if 0 < edad < 120:
            return True
        raise EdadInvalidaError(edad, "La edad ingresada no es válida.")

    def crear_persona(self, nombre: str, edad: int, genero: str, estado_civil: str):
        self.persona = PersonaModel(nombre, edad, genero, estado_civil)
        return self.persona

    def obtener_datos_persona(self):
        if self.persona:
            return self.persona.to_dict()
        return None
