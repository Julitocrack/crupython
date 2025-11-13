import psycopg2
# ⚠️ Importa las excepciones para manejarlas correctamente
from psycopg2 import OperationalError, DatabaseError 

class ConexionBD:
    """
    Clase para manejar la conexión a una base de datos PostgreSQL usando psycopg2.
    """
    def __init__(self):
        # Inicializa la conexión como None
        self.conexion = None
        # Llama a establecerConexionBD en el constructor
        self.establecerConexionBD()

    def establecerConexionBD(self):
        # 📚 Parámetros de conexión para PostgreSQL
        dbname = "crupython"
        user = "postgres"
        # ⚠️ IMPORTANTE: Asegúrate de usar la contraseña correcta.
        # En tu primer código era "1234", pero en el ejemplo de pyodbc era "Jarojmro7".
        # Usaremos "1234" como en tu ejemplo original de psycopg2.
        password = "1234" 
        host = "localhost"
        port = "5432"

        try:
            self.conexion = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("✅ Conexión exitosa a la base de datos PostgreSQL.")
        
        # Capturamos excepciones específicas de psycopg2 para errores de conexión
        except (OperationalError, DatabaseError) as ex:
            print("❌ Error al conectar a la base de datos:")
            print(f"Detalle del error: {ex}")
            self.conexion = None # Asegurarse de que sea None si falla
        except Exception as ex:
            # Capturamos cualquier otra excepción inesperada
            print("❌ Error inesperado durante la conexión:")
            print(f"Detalle del error: {ex}")
            self.conexion = None

    def cerrarConexionBD(self):
        """Cierra la conexión si está abierta."""
        if self.conexion:
            self.conexion.close()
            self.conexion = None
            print("➡️ Conexión a la base de datos cerrada.")