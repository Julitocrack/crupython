class Cliente:
    """Clase de modelo para representar a un Cliente."""
    
    def __init__(self, idCliente=None, dni_rfc=None, nombre=None, direccion=None, telefono=None):
        self.idCliente = idCliente
        self.dni_rfc = dni_rfc
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

    # No se necesitan métodos adicionales si solo se usa para transportar datos (DTO)
