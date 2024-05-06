from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import *
import check
import login
import data_user


class ManagementUser(QMainWindow):
    def __init__(self):
        super(ManagementUser, self).__init__()
        uic.loadUi("management.ui", self)
        self.setWindowTitle("Management User")

        self.setTabOrder(self.line_user_name, self.line_passwd)
        self.setTabOrder(self.line_passwd, self.line_confirm_passwd)
        self.setTabOrder(self.line_confirm_passwd, self.btn_register)
        self.setTabOrder(self.btn_register, self.btn_exit)
        self.setTabOrder(self.btn_exit, self.btn_logout)

        self.setTabOrder(self.line_old_passwd, self.line_new_passwd)
        self.setTabOrder(self.line_new_passwd, self.line_confirm_new_passwd)
        self.setTabOrder(self.line_confirm_new_passwd, self.btn_change_passwd)
        self.setTabOrder(self.btn_change_passwd, self.btn_exit)
        self.setTabOrder(self.btn_exit, self.btn_logout)

        self.line_user_name.returnPressed.connect(self.register_user)
        self.line_passwd.returnPressed.connect(self.register_user)
        self.line_confirm_passwd.returnPressed.connect(self.register_user)
        self.btn_register.setAutoDefault(True)

        self.line_old_passwd.returnPressed.connect(self.change_passwd_admin)
        self.line_new_passwd.returnPressed.connect(self.change_passwd_admin)
        self.line_confirm_new_passwd.returnPressed.connect(self.change_passwd_admin)
        self.btn_change_passwd.setAutoDefault(True)

        self.management_user = data_user.User()
        self.filename_current_row = None
        self.select_row = None

        self.btn_register.clicked.connect(self.register_user)
        self.btn_delete.clicked.connect(self.delete_data)
        self.btn_exit.clicked.connect(self.exit_management)
        self.btn_logout.clicked.connect(self.logout_user)
        self.btn_change_passwd.clicked.connect(self.change_passwd_admin)

        self.table_user.itemSelectionChanged.connect(self.get_select_file)
        self.table_user.setColumnCount(0)
        self.table_user.resizeRowsToContents()

    def register_user(self):
        user_name = self.line_user_name.text()
        passwd = self.line_passwd.text()
        confirm_passwd = self.line_confirm_passwd.text()
        if (user_name or passwd or confirm_passwd) == None:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warring!")
            msgBox.setText("Please enter User Name, Password and Confirm Password")
            msgBox.exec()
        elif self.line_passwd.text() != self.line_confirm_passwd.text():
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warring!")
            msgBox.setText("The password confirmation does not match")
            msgBox.exec()
        elif self.management_user.check_exist_user(str(user_name)) != None:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warring!")
            msgBox.setText("Account already exists")
            msgBox.addButton(QMessageBox.StandardButton.Ok)
            msgBox.exec()
        else:
            self.management_user.insert_data(str(user_name), str(passwd))
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Notification!")
            msgBox.setText("Successfully!")
            msgBox.addButton(QMessageBox.StandardButton.Ok)
            msgBox.exec()
        self.show_data()

    def get_select_file(self):
        self.select_row = self.table_user.currentRow()
        if self.select_row != -1:
            self.filename_current_row = self.table_user.item(self.select_row, 0).text()

    def show_data(self):
        self.table_user.setRowCount(0)
        self.table_user.setColumnCount(2)
        self.management_user.show_data()
        for row_num, row_data in enumerate(self.management_user.data_file):
            self.table_user.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.table_user.setItem(
                    row_num, col_num, QtWidgets.QTableWidgetItem(str(col_data))
                )
        self.table_user.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.table_user.resizeRowsToContents()
        self.table_user.horizontalHeader().setStretchLastSection(True)

    def delete_data(self):
        if self.select_row is None:
            QMessageBox.about(self, "Notifications", "Please choose user")
        elif self.filename_current_row == "admin":
            QMessageBox.about(self, "Notifications", "User admin cannot delete")
        else:
            self.management_user.delete_data(self.filename_current_row)
            self.show_data()

    def change_passwd_admin(self):
        admin = self.management_user.check_exist_user("admin")
        if str(self.line_old_passwd.text()) != admin[1]:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warring!")
            msgBox.setText("Password is incorrect")
        elif self.line_new_passwd.text() != self.line_confirm_new_passwd.text():
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warring!")
            msgBox.setText("The password confirmation does not match")
            msgBox.exec()
        else:
            self.management_user.insert_data("admin", str(self.line_new_passwd.text()))
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Notification!")
            msgBox.setText("Successfully!")
            msgBox.addButton(QMessageBox.StandardButton.Ok)
            msgBox.exec()
            self.show_data()

    def exit_management(self):
        self.hide()
        self.check_ui = check.CheckIntegrity()
        self.check_ui.show()

    def logout_user(self):
        self.hide()
        self.login_ui = login.Login()
        self.login_ui.show()
