from flask_login import UserMixin
from src.db.database import get_db_connection

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        # Adaptado para Postgres/Supabase
        cur.execute("SELECT id, username FROM usuarios WHERE id = %s", (user_id,))
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        
        if user_data:
            return User(id=user_data['id'], username=user_data['username'])
        return None
