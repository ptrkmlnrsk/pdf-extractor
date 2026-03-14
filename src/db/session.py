from sqlalchemy.orm import sessionmaker
from src.db.engine import engine

Session = sessionmaker(bind=engine)
