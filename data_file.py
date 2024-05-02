import sqlite3


class HashData:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.cur = self.conn.cursor()
        self.owner = ""

        self.cur.execute(
            """CREATE TABLE if not exists "table_hash" (
            "File"	TEXT PRIMARY KEY ,
            "SHA1"	TEXT,
            "SHA2"	TEXT,
            "MD5"	TEXT,
            "Owner"  TEXT,
            FOREIGN KEY (Owner) REFERENCES users(User)
            )
            """
        )
        self.conn.commit()

    def show_data(self):
        if self.owner == "admin":
            self.data = self.conn.execute(
                """select * from table_hash ORDER BY CASE WHEN Owner = 'admin' THEN 0 ELSE 1 END, Owner"""
            )
            self.conn.commit()
        else:
            self.data = self.conn.execute(
                """select * from table_hash WHERE Owner=? ORDER BY CASE WHEN Owner = 'admin' THEN 0 ELSE 1 END, Owner""",
                (self.owner,),
            )
            self.conn.commit()

    def insert_data(
        self, file_name, hash_code_sha1, hash_code_sha2, hash_code_md5, owner
    ):
        load_table = """INSERT INTO table_hash(File, SHA1, SHA2, MD5, Owner) 
        VALUES(?,?,?,?,?) 
        ON CONFLICT(File) 
        DO UPDATE SET SHA1=?, SHA2=?, MD5=?
        """
        self.cur.execute(
            load_table,
            (
                file_name,
                hash_code_sha1,
                hash_code_sha2,
                hash_code_md5,
                owner,
                hash_code_sha1,
                hash_code_sha2,
                hash_code_md5,
            ),
        )

    def delete_data(self, file):
        delete_table = "DELETE FROM table_hash WHERE File=?"
        self.cur.execute(delete_table, (file,))
        self.conn.commit()

    def exist_file(self, filename, owner):
        return self.cur.execute(
            """ SELECT File FROM table_hash WHERE File=? AND Owner=?""",
            (filename, owner),
        )

    def get_passwd(self, file):
        self.cur.execute(
            """SELECT user.Password  
                FROM table_hash
                JOIN user ON user.user=table_hash.Owner 
                WHERE table_hash.File = ?""",
            (file,),
        )
        return self.cur.fetchone()
