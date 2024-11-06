class VisualizaError(Exception):
    pass


class EdadInvalidaError(Exception):
    """Excepción lanzada cuando la edad proporcionada no es válida."""

    def __init__(self, edad, mensaje="Edad inválida proporcionada."):
        self.edad = edad
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class RespuestaInvalidaError(VisualizaError):
    """Excepción lanzada cuando la respuesta de voz no es válida."""

    def __init__(self, respuesta, mensaje="Respuesta no válida. Por favor, responda manualmente."):
        self.respuesta = respuesta
        self.mensaje = mensaje
        super().__init__(self.mensaje)
