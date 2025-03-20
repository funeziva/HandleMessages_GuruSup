class InfrastructureException(Exception):
    """
    Exception raised for errors in the infrastructure layer.
    
    Attributes:
        message -- explanation of the error
    """
    
    def __init__(self, message="Error en la infraestructura"):
        self.message = message
        super().__init__(self.message) 