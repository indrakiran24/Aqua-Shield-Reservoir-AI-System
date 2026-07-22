from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL connection
DATABASE_URL = "mysql+pymysql://root:mysql@127.0.0.1:3306/reservoir_ai"

# Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# THIS IS WHAT WAS MISSING
Base = declarative_base()

# Dependency (used by FastAPI routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
