import sqlite3
from datetime import datetime, timedelta
import json

class Database:
    def __init__(self, db_path="chat_history.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add_message(self, user_id: str, role: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO chat_history (user_id, role, content) VALUES (?, ?, ?)",
                (user_id, role, content)
            )

    def get_recent_history(self, user_id: str, limit: int = 5, hours: int = 0.5):
        with sqlite3.connect(self.db_path) as conn:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            cursor = conn.execute(
                """
                SELECT role, content FROM chat_history 
                WHERE user_id = ? AND timestamp > ? 
                ORDER BY timestamp DESC LIMIT ?
                """,
                (user_id, cutoff_time, limit)
            )
            return list(cursor.fetchall())

    def search_history(self, user_id: str, search_term: str = None, 
                      role: str = None, limit: int = 10, hours: int = 24):
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT timestamp, role, content FROM chat_history WHERE user_id = ?"
            params = [user_id]
            
            if hours:
                cutoff_time = datetime.now() - timedelta(hours=hours)
                query += " AND timestamp > ?"
                params.append(cutoff_time)
            
            if search_term:
                query += " AND content LIKE ?"
                params.append(f"%{search_term}%")
                
            if role:
                query += " AND role = ?"
                params.append(role)
                
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            return cursor.fetchall() 