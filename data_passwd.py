import sqlite3


class PasswdFile:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.cur = self.conn.cursor()

        self.cur.execute(
            """CREATE TABLE if not exists "passwd_file" (
            "File"	TEXT PRIMARY KEY ,
            "Password"	TEXT,
            "Owner" TEXT
            )
            """
        )
        self.conn.commit()

    def insert_data(self, file_name, passwd, owner):
        load_table = """INSERT INTO passwd_file(File, Password, Owner) 
        VALUES(?,?,?)
        ON CONFLICT(File)
        DO UPDATE SET Password=?, Owner=? 
        """
        self.cur.execute(
            load_table,
            (file_name, passwd, owner, passwd, owner),
        )
        self.conn.commit()

    def get_passwd(self, file_name, user):
        if user == "admin":
            self.cur.execute(
                """SELECT Password
                FROM passwd_file 
                WHERE File = ?""",
                (file_name,),
            )
            return self.cur.fetchone()
        else:
            self.cur.execute(
                """SELECT Password
                FROM passwd_file 
                WHERE File = ? AND Owner=?""",
                (
                    file_name,
                    user,
                ),
            )
            return self.cur.fetchone()
