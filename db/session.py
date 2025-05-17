# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from core.settings import settings

# Должно быть ДО создания Base
Base = declarative_base()

# Создаем engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init():
    # Импорт моделей должен быть здесь, после объявления Base
    from models.user import User  # noqa
    Base.metadata.create_all(bind=engine)