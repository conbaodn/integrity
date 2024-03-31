import sqlite3


class HashData:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.cur = self.conn.cursor()

        self.cur.execute(
            """CREATE TABLE if not exists "table_hash" (
			"File"	TEXT PRIMARY KEY ,
			"Hash"	TEXT)
			"""
        )

    def show_data(self):
        self.data = self.conn.execute("""select * from table_hash""")
        self.conn.commit()

    def insert_data(self, file_name, hash_code):
        load_table = "INSERT INTO table_hash(File,Hash) VALUES(?,?)ON CONFLICT(File) DO UPDATE SET Hash=?"
        self.cur.execute(load_table, (file_name, hash_code, hash_code))
        self.conn.commit()

    def delete_data(self, File):
        delete_table = "DELETE FROM table_hash WHERE File=?"
        self.cur.execute(delete_table, (File,))
        self.conn.commit()
