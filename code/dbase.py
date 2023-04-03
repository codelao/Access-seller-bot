import sqlite3


class Database:
    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file, check_same_thread=False)
        self.con.cursor().execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, hash TEXT, address TEXT)")
        self.con.cursor().execute("CREATE TABLE IF NOT EXISTS hashes(hash TEXT)")
        self.con.cursor().execute("CREATE TABLE IF NOT EXISTS messages(user_id INTEGER, message TEXT)")
    
    def get_user_address(self, user_id):
        with self.con:
            result = self.con.cursor().execute("SELECT address FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
            return result

    def check_user_hash(self, user_id):
        with self.con:
            result = self.con.cursor().execute("SELECT hash FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return bool(result)
        
    def check_address(self, address,):
        with self.con:
            result = self.con.cursor().execute("SELECT * FROM users WHERE address = ?", (address,)).fetchall()
            return bool(result)
        
    def add_user(self, user_id, address):
        with self.con:
            self.con.cursor().execute("INSERT INTO users (user_id, address) VALUES (?, ?)", (user_id, address,))

    def update_user_address(self, user_id, address):
        with self.con:
            self.con.cursor().execute("UPDATE users SET address = ? WHERE user_id = ?", (user_id, address,))

    def add_hash(self, hash):
        with self.con:
            self.con.cursor().execute("INSERT INTO hashes VALUES (?)", (hash,))

    def add_user_hash(self, user_id, hash):
        with self.con:
            self.con.cursor().execute("UPDATE users SET hash = ? WHERE user_id = ?", (user_id, hash,))
    
    def check_hash(self, hash):
        with self.con:
            result = self.con.cursor().execute("SELECT * FROM hashes WHERE hash = ?", (hash,)).fetchall()
            return bool(result)
        
    def check_user(self, user_id):
        with self.con:
            result = self.con.cursor().execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(result)