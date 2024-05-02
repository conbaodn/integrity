import sqlite3


class User:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.cur = self.conn.cursor()

        self.cur.execute(
            """CREATE TABLE if not exists "user" (
			"User"	TEXT PRIMARY KEY ,
			"Password"	TEXT)
			"""
        )
        self.conn.commit()

    def show_data(self):
        self.data_file = self.conn.execute("""select * from user""")
        self.conn.commit()

    def check_login(self, user_name, passwd):
        login = "select * from user where User = ? and Password = ?"
        self.cur.execute(login, (user_name, passwd))
        self.conn.commit()
        return self.cur.fetchone()

    def check_exist_user(self, user_name):
        exist_user = "select * from user where User = ?"
        self.cur.execute(exist_user, (user_name,))
        self.conn.commit()
        return self.cur.fetchone()

    def insert_data(self, user_name, passwd):
        insert_table = "INSERT INTO user(User,Password) VALUES(?,?) ON CONFLICT(User) DO UPDATE SET Password=?"
        self.cur.execute(insert_table, (user_name, passwd, passwd))
        self.conn.commit()

    def delete_data(self, User):
        delete_table = "DELETE FROM user WHERE User=?"
        self.cur.execute(delete_table, (User,))
        self.conn.commit()
