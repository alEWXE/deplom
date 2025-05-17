from fastapi import APIRouter, HTTPException, Depends, Form, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker, declarative_base
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from pathlib import Path

templates = Jinja2Templates(directory="templates")

# Конфигурация
SECRET_KEY = "your-secret-key-keep-it-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# База данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель пользователя
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    
# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Pydantic схемы
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Настройки безопасности
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Хелперы
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Зависимости
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Модифицируем POST-эндпоинты для работы с формами
@router.post("/register", response_class=RedirectResponse)
async def register_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    db = Depends(get_db)
):
    try:
        # Ваша существующая логика регистрации
        existing_user = db.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()
        
        if existing_user:
            return RedirectResponse("/register?error=Email+already+exists", status_code=status.HTTP_303_SEE_OTHER)
        
        hashed_password = get_password_hash(password)
        db_user = User(
            email=email,
            password=hashed_password,
            name=name
        )
        db.add(db_user)
        db.commit()
        
        # Создаем токен и перенаправляем
        access_token = create_access_token(data={"sub": email})
        response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
        
    except Exception as e:
        return RedirectResponse(f"/register?error={str(e)}", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/login", response_class=RedirectResponse)
async def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db = Depends(get_db)
):
    try:
        db_user = db.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()
        
        if not db_user or not verify_password(password, db_user.password):
            return RedirectResponse("/login?error=Invalid+credentials", status_code=status.HTTP_303_SEE_OTHER)
        
        access_token = create_access_token(data={"sub": email})
        response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
        
    except Exception as e:
        return RedirectResponse(f"/login?error={str(e)}", status_code=status.HTTP_303_SEE_OTHER)