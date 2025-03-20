class DomainException(Exception):
    """
    Exception raised for errors in the domain layer.
    
    Attributes:
        message -- explanation of the error
    """
    
    def __init__(self, message="Error en el dominio"):
        self.message = message
        super().__init__(self.message) 