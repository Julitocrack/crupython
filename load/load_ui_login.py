import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os 
from load.load_ui_main import Load_ui_main 

class LoginDialog(QtWidgets.QDialog): # Heredamos de QDialog (corregido)
    """Clase que maneja el login y el lanzamiento de la aplicación principal."""
    
    def __init__(self):
        super().__init__()
        
        # Cargar el UI (usando el nombre de archivo de tu traceback)
        uic.loadUi("ui/LoginWindow.ui", self) 
        
        # Configuraciones de la ventana
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal) 
        
        # ASIGNACIÓN DE NOMBRES DE WIDGETS para compatibilidad:
        self.line_usuario = self.lineEdit
        self.line_contrasena = self.lineEdit_2
        self.boton_ingresar = self.pushButton
        
        # Configuraciones de widgets
        self.line_contrasena.setEchoMode(QtWidgets.QLineEdit.Password) 

        # Conexiones
        self.boton_ingresar.clicked.connect(self.verificar_credenciales) 
        self.boton_cancelar.clicked.connect(lambda: QtWidgets.QApplication.instance().quit())
        
        # Referencia para la ventana principal
        self.main_window = None

    
    def verificar_credenciales(self):
        """Verifica las credenciales. Si son correctas, lanza la ventana principal."""
        
        usuario = self.line_usuario.text()
        contrasena = self.line_contrasena.text()
        
        if usuario == "admin" and contrasena == "123":
            
            # 1. Ocultar la ventana de login (no cerrarla)
            self.hide()
            
            # 2. Crear y mostrar la ventana principal (Menú)
            # 💡 PASAMOS 'self' (la instancia del Login) a la ventana principal.
            self.main_window = Load_ui_main(login_window=self) 
            self.main_window.show()
            
            # 3. Conexión de Cierre: Al cerrar la principal, cerramos la app.
            self.main_window.destroyed.connect(self.cerrar_aplicacion)
            
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error de Login', 'Usuario o contraseña incorrectos. Intente de nuevo.'
            )
            self.line_contrasena.clear()
            self.line_usuario.setFocus()

    def cerrar_aplicacion(self):
        """Termina la aplicación de forma limpia cuando el menú principal se destruye."""
        # Esto asegura que todo el programa se detenga cuando el usuario sale.
        QtWidgets.QApplication.instance().quit()