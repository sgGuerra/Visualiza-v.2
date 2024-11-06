class VisualizaError(Exception):
    pass


class EdadInvalidaError(Exception):
    """Excepción lanzada cuando la edad proporcionada no es válida."""

    def __init__(self, edad, mensaje="Edad inválida proporcionada."):
        self.edad = edad
        self.mensaje = mensaje
        super().__init__(self.mensaje)
