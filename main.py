from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
import sys
import login

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_ui = login.Login()
    login_ui.show()
    app.exec()
