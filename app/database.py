import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


from dotenv import load_dotenv

load_dotenv()


database_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@host.docker.internal:5433/{os.getenv('DB_NAME')}"

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()