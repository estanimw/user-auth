from database import User
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import bcrypt
import jwt

# Secret key for signing JWT tokens (replace this with your own secret key)
SECRET_KEY = "a-secret-key"

# JWT token expiration time (in minutes)
TOKEN_EXPIRATION_MINUTES = 60

# Function to generate JWT token
def create_jwt_token(user_id: int) -> str:
    expiry = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    payload = {"user_id": user_id, "exp": expiry}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Function to verify JWT token and extract user ID
def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            return JSONResponse(status_code=401, content={"message": "Invalid token"})
        return JSONResponse(status_code=200, content={"message": "Authorized"})
    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"message": "Token has expired"})
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=401, content={"message": "Invalid token"})
