from PyQt6 import uic
from PyQt6.QtWidgets import *
import check
import data_user

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('login.ui', self)
        self.check_ui= check.CheckIntegrity()
        self.data = data_user.User()
        self.btn_login.clicked.connect(self.login_account)
        self.check_ui.btn_register.clicked.connect(self.register_form)
    
    def login_account(self):
        user_name = self.line_user_name.text()
        passwd = self.line_passwd.text()
        check = self.data.check_login(user_name,passwd)
        if(check == None):
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warring!")
            msgBox.setText("Incorrect User Name or Password")
            msgBox.exec()
        elif check[0] != 'admin':
            self.close()
            self.check_ui.show()
            self.check_ui.btn_register.hide()
            self.check_ui.tabWidget.removeTab(2)
        else:
            self.close()
            self.check_ui.show()
    
    def register_form(self):
        self.check_ui.hide()
        uic.loadUi('register.ui', self)
        self.show()
        self.btn_register.clicked.connect(self.register_user)
        
    def register_user(self):
        user_name = self.line_user_name.text()
        passwd = self.line_passwd.text()
        print(user_name +' '+ passwd)
        if user_name and passwd != 0:
            self.data.insert_data(user_name,passwd)
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warring!")
            msgBox.setText("Please enter User Name and Password")
            msgBox.exec()
            
