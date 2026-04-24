from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:qaz098@localhost:5432/my_first"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autoflush = False, bind = engine)