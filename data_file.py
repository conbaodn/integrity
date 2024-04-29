import sqlite3


class HashData:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.cur = self.conn.cursor()

        self.cur.execute(
            """CREATE TABLE if not exists "table_hash" (
            "File"	TEXT PRIMARY KEY ,
            "SHA1"	TEXT,
            "SHA2"	TEXT,
            "MD5"	TEXT
            )
            """
        )

    def show_data(self):
        self.data = self.conn.execute("""select * from table_hash""")
        self.conn.commit()

    def insert_data(self, file_name, hash_code_sha1, hash_code_sha2, hash_code_md5):
        load_table = """INSERT INTO table_hash(File, SHA1, SHA2, MD5) VALUES(?,?,?,?) ON CONFLICT(File) DO UPDATE SET SHA1=?, SHA2=?, MD5=?
        """
        self.cur.execute(
            load_table,
            (
                file_name,
                hash_code_sha1,
                hash_code_sha2,
                hash_code_md5,
                hash_code_sha1,
                hash_code_sha2,
                hash_code_md5,
            ),
        )

    def delete_data(self, File):
        delete_table = "DELETE FROM table_hash WHERE File=?"
        self.cur.execute(delete_table, (File,))
        self.conn.commit()
