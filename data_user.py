import sqlite3

class User():
	def __init__(self):
		self.conn = sqlite3.connect('user.db')
		self.cur = self.conn.cursor()
		
		self.cur.execute("""CREATE TABLE if not exists "user" (
			"User"	TEXT PRIMARY KEY ,
			"Password"	TEXT)
			""")
		
	def set_data(self):
		self.data_file = self.conn.execute("""select * from user""")
	
	def check_login(self,user_name,passwd):
		login = "select * from user where User = ? and Password = ?"
		self.cur.execute(login,(user_name,passwd))
		check = self.cur.fetchone()
		return check
			
	def insert_data(self,user_name,passwd):
		insert_table = "INSERT INTO user(User,Password) VALUES(?,?)ON CONFLICT(User) DO UPDATE SET Password=?"
		self.cur.execute(insert_table,(user_name,passwd,passwd))

	def delete_data(self,User):
		delete_table = "DELETE FROM user WHERE User=?"
		self.cur.execute(delete_table,(User,))