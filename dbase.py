import sqlite3


class Database:
    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file, check_same_thread=False)
        self.con.cursor().execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER UNIQUE, address TEXT UNIQUE, hash TEXT UNIQUE, access TEXT)")
        self.con.cursor().execute("CREATE TABLE IF NOT EXISTS hashes(hash TEXT UNIQUE)")
        self.con.cursor().execute("CREATE TABLE IF NOT EXISTS blocked(user_id INTEGER UNIQUE)")
        self.con.cursor().execute("CREATE TABLE IF NOT EXISTS feedbacks(user_id INTEGER PRIMARY KEY, username TEXT)")

    def get_user_address(self, user_id):
        with self.con:
            return self.con.cursor().execute("SELECT address FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]

    def check_user_hash(self, user_id):
        with self.con:
            return self.con.cursor().execute("SELECT hash FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        
    def check_address(self, address,):
        with self.con:
            result = self.con.cursor().execute("SELECT * FROM users WHERE address = ?", (address,)).fetchone()
            return bool(result)
        
    def add_user(self, user_id, address, access):
        with self.con:
            self.con.cursor().execute("INSERT INTO users (user_id, address, access) VALUES (?, ?, ?)", (user_id, address, access,))

    def add_user_address(self, address, user_id):
        with self.con:
            self.con.cursor().execute("UPDATE users SET address = ? WHERE user_id = ?", (address, user_id,))

    def add_user_hash(self, hash, user_id):
        with self.con:
            self.con.cursor().execute("UPDATE users SET hash = ? WHERE user_id = ?", (hash, user_id,))

    def add_user_access_status(self, access, user_id):
        with self.con:
            self.con.cursor().execute("UPDATE users SET access = ? WHERE user_id = ?", (access, user_id,))

    def check_user_access_status(self, user_id):
        with self.con:
            return self.con.cursor().execute("SELECT access FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]

    def add_hash(self, hash):
        with self.con:
            self.con.cursor().execute("INSERT OR REPLACE INTO hashes VALUES (?)", (hash,))

    def check_hash(self, hash):
        with self.con:
            result = self.con.cursor().execute("SELECT * FROM hashes WHERE hash = ?", (hash,)).fetchone()
            return bool(result)
        
    def check_user(self, user_id):
        with self.con:
            result = self.con.cursor().execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return bool(result)
        
    def payments_count(self):
        with self.con:
            result = self.con.cursor().execute("SELECT * FROM hashes").fetchall()
            return len(result)

    def block_user(self, user_id):
        with self.con:
            self.con.cursor().execute("INSERT INTO blocked VALUES (?)", (user_id,))

    def unblock_user(self, user_id):
        with self.con:
            self.con.cursor().execute("DELETE FROM blocked WHERE user_id = ?", (user_id,))

    def check_if_blocked(self, user_id):
        with self.con:
            result = self.con.cursor().execute("SELECT * FROM blocked WHERE user_id = ?", (user_id,)).fetchone()
            return bool(result)
        
    def get_all_users(self):
        with self.con:
            return self.con.cursor().execute("SELECT user_id FROM users").fetchall()
        
    def add_user_msg(self, user_id, username):
        with self.con:
            self.con.cursor().execute("INSERT INTO feedbacks VALUES (?, ?)", (user_id, username,))
        
    def check_user_msg(self, user_id):
        with self.con:
            return self.con.cursor().execute("SELECT * FROM feedbacks WHERE user_id = ?", (user_id,)).fetchone()
                
    def remove_user_msg(self, user_id):
        with self.con:
            self.con.cursor().execute("DELETE FROM feedbacks WHERE user_id = ?", (user_id,))
