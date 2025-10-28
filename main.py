from PyQt5 import QtWidgets
import sys
from load.load_ui_login import LoginDialog

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LoginDialog()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()

    