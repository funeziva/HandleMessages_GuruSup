class ApplicationException(Exception):
    """
    Excepción base para la capa de Aplicación.
    """
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(f"ApplicationException: {message}")
        self.original_exception = original_exception
