from PyQt6 import uic
from PyQt6.QtWidgets import *
import check
import data_user


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi("login.ui", self)
        self.data_user = data_user.User()
        self.btn_login.clicked.connect(self.login_account)

    def login_account(self):
        user_name = self.line_user_name.text()
        passwd = self.line_passwd.text()
        check_exist = self.data_user.check_login(user_name, passwd)

        if check_exist == None:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warring!")
            msgBox.setText("Incorrect User Name or Password")
            msgBox.addButton(QMessageBox.StandardButton.Ok)
            msgBox.exec()
        elif check_exist[0] != "admin":
            self.hide()
            self.check_ui = check.CheckIntegrity()
            self.check_ui.btn_management.hide()
            self.check_ui.show()

        else:
            self.hide()
            self.check_ui = check.CheckIntegrity()
            self.check_ui.show()
