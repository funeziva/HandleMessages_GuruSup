class InfrastructureException(Exception):
    """
    Excepción base para la capa de Infraestructura.
    """
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(f"InfrastructureException: {message}")
        self.original_exception = original_exception
