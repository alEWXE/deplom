from schemas.auth import Token
from models.user import User
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"

class AuthService:
    def register(self, user: User) -> Token:
        return self._create_token(user)

    def login(self, user: User) -> Token:
        return self._create_token(user)

    def _create_token(self, user: User) -> Token:
        payload = {
            "sub": str(user["_id"]),
            "email": user["email"],
            "exp": datetime.utcnow() + timedelta(hours=10),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return Token(access_token=token)
