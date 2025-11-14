# 1.- Importar librerias
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets, uic 
from modelo.productodao import ProductoDAO

class Load_ui_productos(QtWidgets.QMainWindow):
    
    # 💡 MODIFICACIÓN: Agregamos main_window=None para recibir la referencia del menú principal
    def __init__(self, main_window=None):
        super().__init__()
        
        self.main_window = main_window # Guardamos la referencia del menú
        self.productodao = ProductoDAO()
        self.productodao.producto.idProducto = None # Inicializar ID
        
        # Cargar archivo .ui
        uic.loadUi("ui/ui_productos.ui", self)
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

        self.boton_accion_agregar.clicked.connect(self.guardar_producto)
        self.boton_accion_refrescar.clicked.connect(self.llenar_tabla)
        self.boton_accion_actualizar.clicked.connect(self.actualizar_producto)
        self.boton_accion_eliminar.clicked.connect(self.eliminar_producto)
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

    def guardar_producto(self):
        self.productodao.producto.clave = self.sku_agregar.text()
        self.productodao.producto.descripcion = self.descripcion_agregar.text()
        self.productodao.producto.existencia = int(self.existencia_agregar.text())
        self.productodao.producto.precio = float(self.precio_agregar.text().replace(",", "."))

        self.productodao.insertarProducto()

        self.mensaje.setText("El producto ha sido registrado!!!")
        self.sku_agregar.setText("")
        self.descripcion_agregar.setText("")
        self.existencia_agregar.setText("")
        self.precio_agregar.setText("")


    def llenar_tabla(self):
        datos = self.productodao.listarProductos()
        self.tabla_productos.setRowCount(len(datos))
        fila = 0

        for item in datos:
            self.tabla_productos.setItem(fila,0,QtWidgets.QTableWidgetItem(item[1])) # Clave
            self.tabla_productos.setItem(fila,1,QtWidgets.QTableWidgetItem(item[2])) # Descripción
            self.tabla_productos.setItem(fila,2,QtWidgets.QTableWidgetItem(str(item[3]))) # Existencia
            self.tabla_productos.setItem(fila,3,QtWidgets.QTableWidgetItem(str(item[4]))) # Precio
            fila += 1
    
    
    def actualizar_producto(self):
        """Actualiza el producto en la BD usando los datos del formulario de actualizar."""
        if self.productodao.producto.idProducto is None:
            self.mensaje.setText("ERROR: Primero busca el producto a actualizar.")
            return

        self.productodao.producto.clave = self.sku_actualizar.text()
        self.productodao.producto.descripcion = self.deescripcion_actualizar.text()
        self.productodao.producto.existencia = int(self.existencia_actualizar.text())
        self.productodao.producto.precio = float(self.precio_actualizar.text())

        self.productodao.actualizarProducto()        

        self.mensaje.setText(f"Producto {self.productodao.producto.clave} actualizado correctamente!")
        self.sku_actualizar.setText("")
        self.deescripcion_actualizar.setText("")
        self.existencia_actualizar.setText("")
        self.precio_actualizar.setText("")
        self.productodao.producto.idProducto = None # Limpiar ID


    def eliminar_producto(self):
        """Elimina el producto cargado en la BD."""
        if self.productodao.producto.idProducto is None:
            self.mensaje.setText("ERROR: Primero busca el producto a eliminar.")
            return

        self.productodao.eliminarProducto()

        self.mensaje.setText("El producto ha sido ELIMINADO!")
        self.sku_eliminar.setText("")
        self.descripcion_eliminar.setText("")
        self.existencia_eliminar.setText("")
        self.precio_eliminar.setText("")
        self.productodao.producto.idProducto = None # Limpiar ID

    
    def limpiar_formulario(self):
        self.sku_buscar.setText('')
        self.descripcion_buscar.setText('')
        self.existencia_buscar.setText('')
        self.precio_buscar.setText('')


    def buscar_actualizar(self):
        """Busca producto por SKU y carga sus datos en los campos de Actualizar."""
        clave_a_buscar = self.sku_actualizar.text()
        self.productodao.producto.clave = clave_a_buscar
        datos = self.productodao.buscarProductos()
        
        if len(datos) == 0:
            self.mensaje.setText("SKU no Existe para Actualizar!")
            self.deescripcion_actualizar.setText("")
            self.existencia_actualizar.setText("")
            self.precio_actualizar.setText("")
            self.productodao.producto.idProducto = None
        else:
            self.productodao.producto.idProducto = datos[0][0] # Guardar ID para actualizar
            self.deescripcion_actualizar.setText(datos[0][2])
            self.existencia_actualizar.setText(str(datos[0][3]))
            self.precio_actualizar.setText(str(datos[0][4]))
            self.mensaje.setText(f"Producto {clave_a_buscar} cargado para actualizar.")


    def buscar_eliminar(self):
        """Busca producto por SKU y carga sus datos en los campos de Eliminar."""
        clave_a_buscar = self.sku_eliminar.text()
        self.productodao.producto.clave = clave_a_buscar
        datos = self.productodao.buscarProductos()
        
        if len(datos) == 0:
            self.mensaje.setText("SKU no Existe para Eliminar!")
            self.descripcion_eliminar.setText("")
            self.existencia_eliminar.setText("")
            self.precio_eliminar.setText("")
            self.productodao.producto.idProducto = None
        else:
            self.productodao.producto.idProducto = datos[0][0] # Guardar ID para eliminar
            self.descripcion_eliminar.setText(datos[0][2])
            self.existencia_eliminar.setText(str(datos[0][3]))
            self.precio_eliminar.setText(str(datos[0][4]))
            self.mensaje.setText(f"Producto {clave_a_buscar} listo para eliminar.")


    def buscar_buscar(self):
        """Busca un producto y carga sus datos en los campos de búsqueda."""
        self.productodao.producto.clave = self.sku_buscar.text()
        datos = self.productodao.buscarProductos()
        if len(datos)==0:
            self.mensaje.setText("SKU no Existe!")
        else:
            self.descripcion_buscar.setText(datos[0][2])
            self.existencia_buscar.setText(str(datos[0][3]))
            self.precio_buscar.setText(str(datos[0][4]))

       
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
            self.animacionb