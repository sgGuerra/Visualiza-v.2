class PersonaModel:
    def __init__(self, nombre: str, edad: int, genero: str, estado_civil: str):
        self.nombre: str = nombre
        self.genero: str = genero
        self.edad: int = edad
        self.estado_civil: str = estado_civil

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'genero': self.genero,
            'edad': self.edad,
            'estado_civil': self.estado_civil
        }
