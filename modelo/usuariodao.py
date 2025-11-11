# # En modelo/usuariodao.py
# from .usuario import Usuario # El punto (.) significa 'en la misma carpeta'

# from modelo.conexionbd import ConexionBD
# # ...

# class UsuarioDAO:

#     def __init__(self):
#         # 💡 QUITA: self.bd = ConexionBD() aquí.
#         pass # Solo inicializa atributos si es necesario

#     def buscarUsuario(self, nombre_usuario):
#         """Busca un usuario por nombre, llamando al procedimiento almacenado de PostgreSQL."""
        
#         # 💡 AHORA INICIALIZA LA CONEXIÓN SÓLO CUANDO ES NECESARIO:
#         self.bd = ConexionBD() 
#         self.bd.establecerConexionBD()
        
#         cursor = self.bd.conexion.cursor()
        
#         # ... (resto del código de búsqueda se mantiene)