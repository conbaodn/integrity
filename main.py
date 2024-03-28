from PyQt6 import QtWidgets,  uic
from PyQt6.QtWidgets import *
import sys
import check
import login
        
if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    login_user = login.Login()
    login_user.show()
    app.exec()
