# 1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic  
from modelo.clientedao import ClienteDAO

class Load_ui_clientes(QtWidgets.QMainWindow):
    
    # 💡 MODIFICACIÓN: Agregamos main_window=None para recibir la referencia del menú principal
    def __init__(self, main_window=None):
        super().__init__()
        
        
        self.main_window = main_window # Guardamos la referencia del menú
        self.clientedao = ClienteDAO()
        self.clientedao.cliente.idCliente = None # Inicializar ID
        
        # Cargar archivo .ui (Usando el UI de Productos)
        uic.loadUi("ui/ui_clientes.ui", self)
        # self.show() # Lo quitamos porque ahora se muestra desde main_menu

        # --- Conexiones y Configuraciones ---

        # 3.- Configurar contenedores
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        
        # 💡 CONEXIÓN CORREGIDA: Conecta el botón Salir al nuevo método
        self.boton_salir.clicked.connect(self.cerrar_y_regresar) 
        
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        self.boton_menu.clicked.connect(self.mover_menu)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) 

        # 4.- Conectar botones a funciones
        self.boton_agregar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_agregar))
        self.boton_buscar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_buscar))
        self.boton_actualizar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_actualizar))
        self.boton_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_eliminar))
        self.boton_consultar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_consultar))

        self.boton_accion_agregar.clicked.connect(self.guardar_cliente)
        self.boton_accion_refrescar.clicked.connect(self.llenar_tabla)
        self.boton_accion_actualizar.clicked.connect(self.actualizar_cliente)
        self.boton_accion_eliminar.clicked.connect(self.eliminar_cliente)
        self.boton_accion_limpiar.clicked.connect(self.limpiar_formulario)

        self.boton_buscar_actualizar.clicked.connect(self.buscar_actualizar)
        self.boton_buscar_eliminar.clicked.connect(self.buscar_eliminar)
        self.boton_buscar_buscar.clicked.connect(self.buscar_buscar)


# ------------------------------------------------------------------------------------------------

# 5.- Operaciones con el modelo de datos 

    def cerrar_y_regresar(self):
        """Maneja el cierre de la ventana y el regreso al menú principal."""
        if self.main_window:
            self.main_window.show() # Hacemos visible el menú principal
        
        self.close() # Cerramos la ventana actual

    def guardar_cliente(self):
        # Mapeo: SKU -> DNI/RFC, Descripción -> Nombre, Existencia -> Dirección, Precio -> Teléfono
        self.clientedao.cliente.dni_rfc = self.sku_agregar.text() 
        self.clientedao.cliente.nombre = self.descripcion_agregar.text()
        self.clientedao.cliente.direccion = self.existencia_agregar.text()
        self.clientedao.cliente.telefono = self.precio_agregar.text()

        self.clientedao.insertarCliente()

        self.mensaje.setText("El cliente ha sido registrado!!!")
        self.sku_agregar.setText("")
        self.descripcion_agregar.setText("")
        self.existencia_agregar.setText("")
        self.precio_agregar.setText("")


    def llenar_tabla(self):
        datos = self.clientedao.listarClientes()
        self.tabla_productos.setRowCount(len(datos)) # Usamos tabla_productos
        fila = 0

        for item in datos:
            # Indices: (id, dni_rfc, nombre, direccion, telefono)
            self.tabla_productos.setItem(fila,0,QtWidgets.QTableWidgetItem(item[1])) # DNI/RFC
            self.tabla_productos.setItem(fila,1,QtWidgets.QTableWidgetItem(item[2])) # Nombre
            self.tabla_productos.setItem(fila,2,QtWidgets.QTableWidgetItem(item[3])) # Dirección
            self.tabla_productos.setItem(fila,3,QtWidgets.QTableWidgetItem(item[4])) # Teléfono
            fila += 1
    
    
    def actualizar_cliente(self):
        """Actualiza el cliente en la BD usando los datos del formulario de actualizar."""
        if self.clientedao.cliente.idCliente is None:
            self.mensaje.setText("ERROR: Primero busca el cliente a actualizar.")
            return

        self.clientedao.cliente.dni_rfc = self.sku_actualizar.text()
        self.clientedao.cliente.nombre = self.descripcion_actualizar.text()
        self.clientedao.cliente.direccion = self.existencia_actualizar.text()
        self.clientedao.cliente.telefono = self.precio_actualizar.text()

        self.clientedao.actualizarCliente() 

        self.mensaje.setText(f"Cliente {self.clientedao.cliente.nombre} actualizado correctamente!")
        self.sku_actualizar.setText("")
        self.descripcion_actualizar.setText("")
        self.existencia_actualizar.setText("")
        self.precio_actualizar.setText("")
        self.clientedao.cliente.idCliente = None # Limpiar ID


    def eliminar_cliente(self):
        """Elimina el cliente cargado en la BD."""
        if self.clientedao.cliente.idCliente is None:
            self.mensaje.setText("ERROR: Primero busca el cliente a eliminar.")
            return

        self.clientedao.eliminarCliente()

        self.mensaje.setText("El cliente ha sido ELIMINADO!")
        self.sku_eliminar.setText("")
        self.descripcion_eliminar.setText("")
        self.existencia_eliminar.setText("")
        self.precio_eliminar.setText("")
        self.clientedao.cliente.idCliente = None # Limpiar ID

    
    def limpiar_formulario(self):
        self.sku_buscar.setText('')
        self.descripcion_buscar.setText('')
        self.existencia_buscar.setText('')
        self.precio_buscar.setText('')


    def buscar_actualizar(self):
        """Busca cliente por DNI/RFC y carga sus datos en los campos de Actualizar."""
        clave_a_buscar = self.sku_actualizar.text() # Usamos SKU para DNI/RFC
        self.clientedao.cliente.dni_rfc = clave_a_buscar
        datos = self.clientedao.buscarClientes()
        
        if len(datos) == 0:
            self.mensaje.setText("DNI/RFC no Existe para Actualizar!")
            self.descripcion_actualizar.setText("")
            self.existencia_actualizar.setText("")
            self.precio_actualizar.setText("")
            self.clientedao.cliente.idCliente = None
        else:
            self.clientedao.cliente.idCliente = datos[0][0] # Guardar ID para actualizar
            self.descripcion_actualizar.setText(datos[0][2]) # Nombre
            self.existencia_actualizar.setText(datos[0][3]) # Dirección
            self.precio_actualizar.setText(datos[0][4]) # Teléfono
            self.mensaje.setText(f"Cliente {clave_a_buscar} cargado para actualizar.")


    def buscar_eliminar(self):
        """Busca cliente por DNI/RFC y carga sus datos en los campos de Eliminar."""
        clave_a_buscar = self.sku_eliminar.text() # Usamos SKU para DNI/RFC
        self.clientedao.cliente.dni_rfc = clave_a_buscar
        datos = self.clientedao.buscarClientes()
        
        if len(datos) == 0:
            self.mensaje.setText("DNI/RFC no Existe para Eliminar!")
            self.descripcion_eliminar.setText("")
            self.existencia_eliminar.setText("")
            self.precio_eliminar.setText("")
            self.clientedao.cliente.idCliente = None
        else:
            self.clientedao.cliente.idCliente = datos[0][0] # Guardar ID para eliminar
            self.descripcion_eliminar.setText(datos[0][2]) # Nombre
            self.existencia_eliminar.setText(datos[0][3]) # Dirección
            self.precio_eliminar.setText(datos[0][4]) # Teléfono
            self.mensaje.setText(f"Cliente {clave_a_buscar} listo para eliminar.")


    def buscar_buscar(self):
        """Busca un cliente y carga sus datos en los campos de búsqueda."""
        self.clientedao.cliente.dni_rfc = self.sku_buscar.text() # Usamos SKU para DNI/RFC
        datos = self.clientedao.buscarClientes()
        if len(datos)==0:
            self.mensaje.setText("DNI/RFC no Existe!")
        else:
            self.descripcion_buscar.setText(datos[0][2]) # Nombre
            self.existencia_buscar.setText(datos[0][3]) # Dirección
            self.precio_buscar.setText(datos[0][4]) # Teléfono

       
# ------------------------------------------------------------------------------------------------

# 6.- mover ventana

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()

#7.- Mover menú

    def mover_menu(self):
        if True:			
            width = self.frame_lateral.width()
            widthb = self.boton_menu.width()
            normal = 0
            if width==0:
                extender = 200
                self.boton_menu.setText("Menú")
            else:
                extender = normal
                self.boton_menu.setText("")
                
            self.animacion = QPropertyAnimation(self.frame_lateral, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            
            self.animacionb = QPropertyAnimation(self.boton_menu, b'minimumWidth')
        
            self.animacionb.setStartValue(width)
            self.animacionb.setEndValue(extender)
            self.animacionb.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacionb.start()