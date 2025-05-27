from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 
from dotenv import load_dotenv

load_dotenv()

DB_HOST = "localhost"
DB_PORT = "3306"     
DB_USER = "root"     
DB_PASSWORD = "Carolaine22"
DB_NAME = "api_mercadopago"

DATABASE_URL = "mysql+pymysql://root:Carolaine22@localhost:3306/api_mercadopago"

engine = create_engine(DATABASE_URL) 
SessionLocal = sessionmaker (bind=engine, autoflush=False)
Base = declarative_base()