from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_USERNAME = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "nsunetdb"

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@db:5432/{DB_NAME}"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)


Base.metadata.create_all(bind=engine)
