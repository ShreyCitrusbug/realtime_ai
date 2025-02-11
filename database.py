"""
This file contains all database setup functions for the connection.
"""
# standard libraries
from os import getenv

# third party libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()

engine = create_engine(
    getenv("DATABASE_URL"),
)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
