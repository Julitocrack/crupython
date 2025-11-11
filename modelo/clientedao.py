from modelo.conexionbd import ConexionBD 
from modelo.cliente import Cliente # Necesitarás crear este archivo


class ClienteDAO:


    def __init__(self):
        # Asumiendo que la clase se llama 'ConexionBD' y fue corregida
        self.bd = ConexionBD() 
        self.cliente = Cliente()

    def listarClientes(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Uso de SELECT para llamar a la función de PostgreSQL
        sp = "SELECT * FROM sp_listar_clientes()" 
        cursor.execute(sp)
        filas = cursor.fetchall()

        self.bd.cerrarConexionBD()
        return filas

    def insertarCliente(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Uso de CALL (4 parámetros: dni_rfc, nombre, direccion, telefono)
        sp = "CALL sp_insertar_cliente(?, ?, ?, ?)"
        parametros = (self.cliente.dni_rfc, self.cliente.nombre, self.cliente.direccion, self.cliente.telefono)
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()

        self.bd.cerrarConexionBD()

    def actualizarCliente(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Uso de CALL (5 parámetros: idCliente, dni_rfc, nombre, direccion, telefono)
        sp = "CALL sp_actualizar_cliente(?, ?, ?, ?, ?)"
        parametros = (self.cliente.idCliente, self.cliente.dni_rfc, self.cliente.nombre, self.cliente.direccion, self.cliente.telefono)
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()

        self.bd.cerrarConexionBD()

    def eliminarCliente(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Uso de CALL (1 parámetro: idCliente)
        sp = "CALL sp_eliminar_cliente(?)"
        parametros = (self.cliente.idCliente,) 
        cursor.execute(sp, parametros)
        self.bd.conexion.commit()

        self.bd.cerrarConexionBD()

    
    def contarClientes(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Uso de SELECT para la función que devuelve el conteo
        sp = "SELECT sp_contar_clientes()"
        cursor.execute(sp)
        resultado = cursor.fetchone()

        print(f"Total de clientes: {resultado[0]}")

        self.bd.cerrarConexionBD()
        return resultado[0] # Se retorna el resultado para consistencia

    def buscarClientes(self):

        self.bd.establecerConexionBD()

        cursor = self.bd.conexion.cursor()
        # Uso de SELECT para la función que devuelve la tabla (se busca por dni_rfc)
        sp = "SELECT * FROM sp_buscar_cliente(?)"
        param = [self.cliente.dni_rfc] 
        cursor.execute(sp, param)
        filas = cursor.fetchall()

        self.bd.cerrarConexionBD()
        return filas