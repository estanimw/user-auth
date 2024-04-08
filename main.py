from auth import create_jwt_token, verify_token
from database import SessionLocal, engine, Base, User
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import bcrypt

# Create an instance of FastAPI
app = FastAPI()

# Ensure that all SQLAlchemy models are created
Base.metadata.create_all(bind=engine)

# Pydantic models for data type validations
class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class AuthRequest(BaseModel):
    token: str

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define a route and its corresponding function
@app.get("/")
def landing():
    return {"message": "Hello, World!"}

# Define a route and its corresponding function
@app.post("/api/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(username=user_data.username, first_name=user_data.first_name, last_name=user_data.last_name, email=user_data.email, password=hashed_password.decode('utf-8'))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return JSONResponse(status_code=200, content={"message": "User registered successfully"})

# Define a route and its corresponding function
@app.post("/api/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not bcrypt.checkpw(user_data.password.encode('utf-8'), user.password.encode('utf-8')):
        return JSONResponse(status_code=401, content={"message": "Invalid username or password"})
    token = create_jwt_token(user.id)
    return JSONResponse(status_code=200, content={"message": "Login successful", "token": token})

# Define a route and its corresponding function
@app.post("/api/authorized")
def auth(auth_request: AuthRequest):
    return verify_token(auth_request.token)