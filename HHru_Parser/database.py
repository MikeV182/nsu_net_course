import json

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


with open("dev_config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
DB_USERNAME = config["db_username"]
DB_PASSWORD = config["db_password"]
DB_NAME = config["db_name"]

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    salary = Column(String)
    link = Column(String)
    experience = Column(String)


Base.metadata.create_all(bind=engine)
