from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}' # 'postgressql://<username>:<password>@<ipaddress/hostname>/<dbname>'

# SQLALCHEMY_DB_URL = f'postgresql://fastapi_28wl_user:7Cgtu7xcjHCTfwXxK6zzbvudWV3IzwFz@dpg-ck6tmn88elhc73e432hg-a:5432/fastapi_28wl'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()