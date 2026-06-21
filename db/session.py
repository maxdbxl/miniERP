from sqlalchemy.orm import sessionmaker
from db.database import engine

SessionLocal = sessionmaker(bind=engine)

def get_session():
    with SessionLocal() as session:
        yield session