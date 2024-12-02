from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  create_engine

database_url="postgresql://postgres:mysecretpassword@localhost:5433/transport_system_fastapi"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

