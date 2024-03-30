from PyQt6 import QtWidgets,  uic
from PyQt6.QtWidgets import *
import data_user

class ManagementUser(QMainWindow):
	def __init__(self):
		super(ManagementUser, self).__init__()
		uic.loadUi('management.ui', self)
		
		self.management_user=data_user.User
		self.filename_current_row = None
		self.select_row = None
		
		self.btn_register.clicked.connect(self.register_user)
		self.btn_delete.clicked.connect(self.delete_data)

		self.table_user.itemSelectionChanged.connect(self.get_select_file)
		self.table_user.setColumnCount(0)
		
	def register_user(self):
		user_name = self.line_user_name.text()
		passwd = self.line_passwd.text()
		confirm_passwd = self.line_confirm_passwd.text()
		if user_name or passwd or confirm_passwd == None:
			msgBox = QMessageBox()
			msgBox.setWindowTitle("Warring!")
			msgBox.setText("Please enter User Name, Password and Confirm Password")
			msgBox.exec()
		elif self.line_passwd.text() != self.line_confirm_passwd:
			msgBox = QMessageBox()
			msgBox.setWindowTitle("Warring!")
			msgBox.setText("The password confirmation does not match")
			msgBox.exec()
		else:
			self.management_user.insert_user(str(user_name),str(passwd))
	
	def get_select_file(self):
		self.select_row = self.table_user.currentRow()
		if self.select_row != -1:
			self.filename_current_row = self.table_user.item(self.select_row,0).text()
			
	def show_data(self):
		self.table_user.setRowCount(0)
		self.table_user.setColumnCount(2)  
		self.management_user.show_data()     
		for row_num, row_data in enumerate(self.management_user.data):
			self.table_user.insertRow(row_num)
			for col_num, col_data in enumerate(row_data):
				self.table_user.setItem(row_num,col_num,QtWidgets.QTableWidgetItem(str(col_data)))
				
	def delete_data(self):
		if(self.select_row is None):
			QMessageBox.about(self, "Notifications", "Please choose user")
		else :
			self.management_user.delete_data(self.filename_current_row)
			self.show_data()

