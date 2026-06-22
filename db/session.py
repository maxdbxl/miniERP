from sqlalchemy.orm import sessionmaker
from db.database import engine

SessionLocal = sessionmaker(bind=engine)

def get_session():
    #fix temporaire, à corriger plus tard (with)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()