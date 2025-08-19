import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_database_url():
    """Get database URL based on configuration"""
    if settings.database_type.lower() == "sqlite":
        # SQLite connection string
        db_path = os.path.join(PROJECT_ROOT, settings.sqlite_db_path)
        return f"sqlite:///{db_path}"
    else:
        # SQL Server connection string (default)
        if settings.sqlserver_username and settings.sqlserver_password:
            # SQL Authentication
            if settings.sqlserver_port == 0:
                # Use instance name without port
                return (
                    f"mssql+pyodbc://{settings.sqlserver_username}:{settings.sqlserver_password}"
                    f"@{settings.sqlserver_server}"
                    f"/{settings.sqlserver_database}"
                    f"?driver={settings.sqlserver_driver.replace(' ', '+')}"
                    f"&charset=utf8"
                    f"&autocommit=true"
                    f"&unicode_results=true"
                )
            else:
                # Use specific port
                return (
                    f"mssql+pyodbc://{settings.sqlserver_username}:{settings.sqlserver_password}"
                    f"@{settings.sqlserver_server}:{settings.sqlserver_port}"
                    f"/{settings.sqlserver_database}"
                    f"?driver={settings.sqlserver_driver.replace(' ', '+')}"
                    f"&charset=utf8"
                    f"&autocommit=true"
                    f"&unicode_results=true"
                )
        else:
            # Windows Authentication
            if settings.sqlserver_port == 0:
                # Use instance name without port
                return (
                    f"mssql+pyodbc://@{settings.sqlserver_server}"
                    f"/{settings.sqlserver_database}"
                    f"?driver={settings.sqlserver_driver.replace(' ', '+')}"
                    f"&charset=utf8"
                    f"&autocommit=true"
                    f"&unicode_results=true"
                    f"&trusted_connection=yes"
                )
            else:
                # Use specific port
                return (
                    f"mssql+pyodbc://@{settings.sqlserver_server}:{settings.sqlserver_port}"
                    f"/{settings.sqlserver_database}"
                    f"?driver={settings.sqlserver_driver.replace(' ', '+')}"
                    f"&charset=utf8"
                    f"&autocommit=true"
                    f"&unicode_results=true"
                    f"&trusted_connection=yes"
                )

def get_engine_kwargs():
    """Get engine kwargs based on database type"""
    if settings.database_type.lower() == "sqlite":
        return {
            "connect_args": {"check_same_thread": False},
            "echo": settings.environment == "development"
        }
    else:
        # SQL Server (default)
        return {
            "echo": settings.environment == "development",
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "connect_args": {
                "charset": "utf8",
                "use_unicode": True,
                "unicode_results": True
            }
        }

SQLALCHEMY_DATABASE_URL = get_database_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL, **get_engine_kwargs())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 