import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Settings:
    # OCR Settings
    tesseract_path: str = os.getenv("TESSERACT_PATH", r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
    default_lang: str = os.getenv("TESS_LANG", "vie+eng")
    
    # Database Settings
    database_type: str = os.getenv("DATABASE_TYPE", "sqlserver")  # sqlserver or sqlite
    
    # SQLite Settings
    sqlite_db_path: str = os.getenv("SQLITE_DB_PATH", "contracts.db")
    
    # SQL Server Settings (Default)
    sqlserver_server: str = os.getenv("SQLSERVER_SERVER", "localhost")  # Sử dụng instance mặc định
    sqlserver_database: str = os.getenv("SQLSERVER_DATABASE", "SH_HopDong")
    sqlserver_username: str = os.getenv("SQLSERVER_USERNAME", "")  # Để trống để sử dụng Windows Authentication
    sqlserver_password: str = os.getenv("SQLSERVER_PASSWORD", "")  # Để trống để sử dụng Windows Authentication
    sqlserver_port: int = int(os.getenv("SQLSERVER_PORT", "0"))  # 0 = use default port
    sqlserver_driver: str = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 17 for SQL Server")
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")


settings = Settings() 