import atexit
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, func

USER_POSTGRES = os.getenv("USER_POSTGRES", "postgres")
PASSWORD_POSTGRES = os.getenv("PASSWORD_POSTGRES", "Nervnii39")
DB_POSTGRES = os.getenv("DB_POSTGRES", "flask_db")
HOST_POSTGRES = os.getenv("HOST_POSTGRES", "127.0.0.1")
PORT_POSTGRES = os.getenv("PORT_POSTGRES", "5431")

DSN = f"postgresql://{USER_POSTGRES}:{PASSWORD_POSTGRES}@{HOST_POSTGRES}:{PORT_POSTGRES}/{DB_POSTGRES}"
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

atexit.register(engine.dispose)


class Advertisment(Base):
    __tablename__ = "flask_app_advertisment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, index=True, unique=True)
    text = Column(Text)
    author = Column(String, nullable=False)
    creation_date = Column(DateTime, server_default=func.now())


Base.metadata.create_all()