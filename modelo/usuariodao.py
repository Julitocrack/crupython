# En modelo/usuariodao.py

# Ya no necesitamos importar bcrypt aquí
from modelo.conexionbd import ConexionBD
from modelo.usuario import Usuario 

class UsuarioDAO:

    def __init__(self):
        self.bd = ConexionBD()
        self.usuario = Usuario()

    def buscarUsuario(self, nombre_usuario):
        """Busca un usuario por nombre, llamando al procedimiento almacenado."""
        self.bd.establecerConexionBD()
        
        cursor = self.bd.conexion.cursor()
        
        # 💡 CORRECCIÓN CLAVE: Usamos SELECT * FROM para llamar a la función/SP
        sql = "SELECT * FROM sp_buscar_usuario(?);"
        parametros = (nombre_usuario,)

        cursor.execute(sql, parametros)
        fila = cursor.fetchone()
        
        self.bd.cerrarConexionBD()

        if fila:
            # Crea y devuelve un objeto Usuario (Índices: 0=id, 1=nombre, 2=hash)
            return Usuario(idUsuario=fila[0], nombre_usuario=fila[1], password_hash=fila[2])
        return None