from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import *
import hashlib
import data_file
import md5
import login
import management


class CheckIntegrity(QMainWindow):
    def __init__(self):
        super(CheckIntegrity, self).__init__()
        uic.loadUi("check.ui", self)

        self.data = data_file.HashData()
        self.management_user = management.ManagementUser()
        self.filename_current_row = None
        self.select_row = None

        self.btn_choose.clicked.connect(self.process_hash)
        self.btn_file_check.clicked.connect(self.open_file_check)
        self.btn_save.clicked.connect(self.save_text_hash)
        self.btn_check.clicked.connect(self.check_integrity)
        self.btn_show_data.clicked.connect(self.show_data)
        self.btn_load.clicked.connect(self.process_load_data)
        self.btn_delete.clicked.connect(self.delete_data)
        self.btn_check_data.clicked.connect(self.check_by_data)
        self.btn_management.clicked.connect(self.management_form)
        self.btn_logout.clicked.connect(self.logout_user)

        self.table_file_hash.itemSelectionChanged.connect(self.get_select_file)
        self.table_file_hash.setColumnCount(0)

    def process_hash(self):
        data = self.open_file()
        if data is not None:
            self.line_choose.setText(data[0])
            hash_text = self.hash_function(data[0])
            self.text_hash_sha1.setText(hash_text[0])
            self.text_hash_sha2.setText(hash_text[1])
            self.text_hash_md5.setText(hash_text[2])

    def save_text_hash(self):
        text = (
            self.text_hash_sha1.toPlainText()
            + self.text_hash_sha2.toPlainText()
            + self.text_hash_md5.toPlainText()
        )
        self.filename = QFileDialog.getSaveFileName(self, "Save")
        if self.filename[0] != "":
            fp = open(self.filename[0], "w")
            fp.writelines(text)

    def open_file_check(self):
        try:
            data = self.open_file()
            if data is not None:
                self.line_file_check_1.setText(data[0])
                self.text_check_sha1_1.setText(data[1].decode("utf-8")[0:40])
                self.text_check_sha2_1.setText(data[1].decode("utf-8")[40:104])
                self.text_check_md5_1.setText(data[1].decode("utf-8")[104:])
                self.label_file_check.setText(
                    "<font color='red'>Check from file:</font>"
                )
        except:
            QMessageBox.about(self, "Notifications", "File check is incorrect!")

    def check_integrity(self):
        if self.line_choose.text() == "":
            QMessageBox.about(self, "Notifications", "Please choose the file!")

        elif self.line_file_check_1.text() == "":
            QMessageBox.about(self, "Notifications", "Please choose the file check!")

        elif (
            len(
                self.text_check_sha1_1.toPlainText()
                + self.text_check_sha2_1.toPlainText()
                + self.text_check_md5_1.toPlainText()
            )
            != 136
        ):
            QMessageBox.about(self, "Notifications", "File check is incorrect!")

        elif (
            self.text_hash_sha1.toPlainText() == self.text_check_sha1_1.toPlainText()
            and self.text_hash_sha2.toPlainText()
            == self.text_check_sha2_1.toPlainText()
            and self.text_hash_md5.toPlainText() == self.text_check_md5_1.toPlainText()
        ):
            QMessageBox.about(self, "Notifications", "File does not change!")

        else:
            QMessageBox.about(self, "Notifications", "File has changed!")

    def hash_function(self, data):
        hash_text_sha1 = hashlib.sha1(data.encode("utf8")).hexdigest()
        hash_text_sha256 = hashlib.sha256(data.encode("utf8")).hexdigest()
        hash_text_md5 = md5.md5(data)

        return hash_text_sha1, hash_text_sha256, hash_text_md5

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, "Open File")

        if filename[0]:
            self.filename = filename[0]
            f = open(filename[0], "rb")
            text = f.read()
            return str(filename[0]), text
        else:
            QMessageBox.about(self, "Notifications", "Please choose file!")

    # Data
    def show_data(self):
        self.table_file_hash.setRowCount(0)
        self.table_file_hash.setColumnCount(2)
        self.data.show_data()
        for row_num, row_data in enumerate(self.data.data):
            self.table_file_hash.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.table_file_hash.setItem(
                    row_num, col_num, QtWidgets.QTableWidgetItem(str(col_data))
                )

    def process_load_data(self):
        self.data.insert_data(
            str(self.line_choose.text()),
            str(
                self.text_hash_sha1.toPlainText()
                + self.text_hash_sha2.toPlainText()
                + self.text_hash_md5.toPlainText()
            ),
        )
        self.show_data()

    def delete_data(self):
        if self.select_row is None:
            QMessageBox.about(self, "Notifications", "Please choose data row!")
        else:
            self.data.delete_data(self.filename_current_row)
            self.show_data()

    def check_by_data(self):
        if self.select_row is None:
            QMessageBox.about(self, "Notifications", "Please choose data row!")
        else:
            hash_text = self.table_file_hash.item(self.select_row, 1).text()
            self.line_file_check_1.setText(
                self.table_file_hash.item(self.select_row, 0).text()
            )
            self.text_check_sha1_1.setText(hash_text[0:40])
            self.text_check_sha2_1.setText(hash_text[40:104])
            self.text_check_md5_1.setText(hash_text[104:])
            self.label_file_check.setText("<font color='red'>Check from data:</font>")

    def get_select_file(self):
        self.select_row = self.table_file_hash.currentRow()
        if self.select_row != -1:
            self.filename_current_row = self.table_file_hash.item(
                self.select_row, 0
            ).text()

    def management_form(self):
        self.hide()
        self.management_user.show_data()
        self.management_user.show()

    def logout_user(self):
        self.hide()
        self.login_ui = login.Login()
        self.login_ui.show()
