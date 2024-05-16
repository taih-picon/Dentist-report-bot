import os 
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class Settings(BaseSettings):
    app_name: str = "Dentis Report Bot"
    allowed_origins : str
    db_host : str
    db_port : str = "5432"
    db_name : str = "postgres"
    db_username : str
    db_password : str
    openai_api_key : str
    openai_llm_model : str

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
settings = Settings()