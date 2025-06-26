from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv() # Carga las variables de entorno del archivo .env

class Settings(BaseSettings):
    # Permite usar MONGODB_URL o MONGODB_URI (para compatibilidad con Docker)
    MONGODB_URI: str = os.getenv("MONGODB_URL", os.getenv("MONGODB_URI", "mongodb://localhost:27017/bank_db"))
    DATABASE_NAME: str = "bank_db"

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()