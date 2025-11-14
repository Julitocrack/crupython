from modelo.conexionbd import ConexionBD # Asumiendo que la clase se llama ConexionBD
from modelo.producto import Producto 


class ProductoDAO:


    def __init__(self):

        # Corregido: Uso de ConexionBD con la D mayúscula
        self.bd = ConexionBD() 
        self.producto = Producto()

    def listarProductos(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Corregido: Uso de SELECT para llamar a la función que devuelve la tabla
        sp = "SELECT * FROM sp_listar_productos()" 
        cursor.execute(sp)
        filas = cursor.fetchall()

        self.bd.cerrarConexionBD()
        return filas

    def insertarProducto(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Corregido: Uso de CALL y solo los placeholders (?)
        sp = "CALL sp_insertar_producto(%s, %s, %s, %s)"
        parametros = (self.producto.clave, self.producto.descripcion, self.producto.existencia, self.producto.precio)
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()

        self.bd.cerrarConexionBD()

    def actualizarProducto(self):

        self.bd.establecerConexionBD()
        cursor = self.bd.conexion.cursor()

        sp = "CALL sp_actualizar_producto(%s, %s, %s, %s, %s)"
        parametros = (
            self.producto.idProducto,
            self.producto.clave,
            self.producto.descripcion,
            self.producto.existencia,
            self.producto.precio
        )

        cursor.execute(sp, parametros)
        self.bd.conexion.commit()

        cursor.close()
        self.bd.cerrarConexionBD()

    def eliminarProducto(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Corregido: Uso de CALL y solo el placeholder (?)
        sp = "CALL sp_eliminar_producto(%s)"
        # Nota: pyodbc espera una tupla, incluso con un solo elemento
        parametros = (self.producto.idProducto,) 
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()

        self.bd.cerrarConexionBD()

    
    def contarProductos(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Corregido: Uso de SELECT para llamar a la función que devuelve un solo valor
        sp = "SELECT sp_contar_productos()"
        cursor.execute(sp)
        resultado = cursor.fetchone()

        print(f"Total de productos: {resultado[0]}")

        self.bd.cerrarConexionBD()

    def buscarProductos(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Corregido: Uso de SELECT para llamar a la función que devuelve la tabla
        sp = "SELECT * FROM sp_buscar_producto(%s)"
        # Nota: la lista o tupla de parámetros para cursor.execute()
        param = [self.producto.clave] 
        cursor.execute(sp, param)
        filas = cursor.fetchall()

        self.bd.cerrarConexionBD()
        return filas