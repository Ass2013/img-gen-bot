import sqlite3
from config import DATABASE


class DatabaseManager:
    def __init__(self, database):
        self.database = database
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                prompt TEXT
            )
        """)

        conn.commit()
        conn.close()

    def save_image(self, username, prompt):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO images (username, prompt)
            VALUES (?, ?)
        """, (username, prompt))

        conn.commit()
        conn.close()

    def get_images(self, username):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT prompt FROM images
            WHERE username = ?
        """, (username,))

        data = cursor.fetchall()
        conn.close()
        return data