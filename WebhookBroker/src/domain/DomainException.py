class DomainException(Exception):
    """
    Excepción base para la capa de Dominio.
    """
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(f"DomainException: {message}")
        self.original_exception = original_exception
