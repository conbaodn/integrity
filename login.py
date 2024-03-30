from PyQt6 import uic
from PyQt6.QtWidgets import *
import check
import data_user

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('login.ui', self)
        self.check_ui= check.CheckIntegrity()
        self.data_user = data_user.User()
        self.btn_login.clicked.connect(self.login_account)
        
    
    def login_account(self):
        user_name = self.line_user_name.text()
        passwd = self.line_passwd.text()
        check = self.data_user.check_exist(user_name,passwd)
        self.data_user.conn.close()

        if(check == None):
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warring!")
            msgBox.setText("Incorrect User Name or Password")
            msgBox.exec()
        elif check[0] != 'admin':
            self.close()
            self.check_ui.show()
            self.check_ui.btn_management.hide()
            self.check_ui.tabWidget.removeTab(2)
        else:
            self.close()
            self.check_ui.show()
    

