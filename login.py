from PyQt6 import QtWidgets,  uic
from PyQt6.QtWidgets import *
import sqlite3
class Login(QMainWindow):
	def __init__(self):
		super(Login, self).__init__()
		uic.loadUi('login.ui', self)
	
		self.conn = sqlite3.connect('login.db')
		self.cur = self.conn.cursor()
		
		self.cur.execute("""CREATE TABLE if not exists "user" (
			"User"	TEXT PRIMARY KEY ,
			"Password"	TEXT)
			""")
	def set_data(self):
		self.data_file = self.conn.execute("""select * from user""")
			
	def load_data(self,file_name,hash_code):
		load_table="INSERT INTO user(User,Password) VALUES(?,?)ON CONFLICT(User) DO UPDATE SET Hash=?"
		self.cur.execute(load_table,(file_name,hash_code,hash_code))

	def delete_data(self,User):
		delete_table = "DELETE FROM user WHERE User=?"
		self.cur.execute(delete_table,(User,))