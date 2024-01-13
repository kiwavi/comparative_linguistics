from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@127:0:0:1/db"  # should add db here

# sqlalchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# represents actual db session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Later we will inherit from this class to create each of the database models or classes (the ORM models):
Base = declarative_base()


