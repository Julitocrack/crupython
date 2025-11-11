import pyodbc

class ConexionBD:
    def __init__(self):
        # 1. Llamar a establecerConexionBD en el constructor
        self.conexion = None
        self.establecerConexionBD()

    def establecerConexionBD(self):
        try:
            self.conexion = pyodbc.connect(
                'DRIVER={PostgreSQL Unicode};'
                'SERVER=localhost;'
                'DATABASE=crupython;'
                'UID=postgres;'             # <-- Usuario de PostgreSQL (Ejemplo)
                'PWD=Jarojmro7;'   # <-- Contraseña de PostgreSQL
            )
            print("Conexion exitosa")
        except Exception as ex:
            print("Error al conectar a la base de datos: " + str(ex))
            self.conexion = None # Asegurarse de que sea None si falla

    
    def cerrarConexionBD(self):
        if self.conexion:
            self.conexion.close()
            self.conexion = None