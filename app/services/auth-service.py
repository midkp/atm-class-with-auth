import jwt
from app.core.settings import SECRET_KEY
from app.dependencies.database import get_db_connection

class AuthService:
    def __init__(self):
        self.conn = get_db_connection()
    
    def authenticate_user(self, username, pin):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ? AND pin = ?", (username, pin))
        user = cursor.fetchone()
        if user:
            token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
            return {"token": token}
        return {"error": "Invalid username or PIN"}
