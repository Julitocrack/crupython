import os 
from PyQt5 import QtCore, QtGui, QtWidgets, uic  
from load.load_ui_productos import Load_ui_productos 
from load.load_ui_clientes import Load_ui_clientes 

class Load_ui_main(QtWidgets.QMainWindow):
    
    # 💡 CAMBIO: Recibimos login_window=None en el constructor
    def __init__(self, login_window=None):
        super().__init__()
        
        uic.loadUi("ui/ui_main_menu.ui", self) 
        
        self.login_window = login_window # 💡 Guardamos la referencia del Login
        self.productos_window = None
        self.clientes_window = None

        # Conexiones de los botones de navegación
        self.boton_productos.clicked.connect(self.abrir_productos)
        self.boton_clientes.clicked.connect(self.abrir_clientes)
        
        # 💡 CONEXIÓN CRÍTICA: Conectamos Cerrar Sesión al método de regreso.
        self.boton_cerrar_sesion.clicked.connect(self.cerrar_sesion_y_regresar) 

    # --- Métodos de Navegación (Se mantienen) ---

    def abrir_productos(self):
        self.hide()
        
        self.productos_window = Load_ui_productos(main_window=self) 
        self.productos_window.show() 
        
        self.productos_window.destroyed.connect(self.regresar_a_menu)


    def abrir_clientes(self):
        self.hide()
        
        self.clientes_window = Load_ui_clientes(main_window=self)
        self.clientes_window.show()
        
        self.clientes_window.destroyed.connect(self.regresar_a_menu)

        
    def regresar_a_menu(self):
        """Muestra el menú principal de nuevo después de que un módulo se cierra."""
        self.show()

    # --- Nuevo Método de Cerrar Sesión ---
    def cerrar_sesion_y_regresar(self):
        """Oculta el menú principal y vuelve a mostrar la ventana de Login."""
        
        # 1. Ocultar la ventana actual (Menú Principal)
        self.hide()
        
        # 2. Si la referencia al login existe, la mostramos y limpiamos campos.
        if self.login_window:
            # Limpiamos los campos antes de reaparecer
            self.login_window.line_usuario.clear()
            self.login_window.line_contrasena.clear()
            self.login_window.show()
            
        # 3. Cerramos la ventana de menú, lo que disparará la señal destroyed
        # para que el QApplication pueda limpiarse.
        self.close()