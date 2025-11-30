from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator
from app.core.config import settings

# MySQL Database
# Fix for Railway/Cloud: Ensure we use pymysql driver
db_url = settings.DATABASE_URL

# Support for different database types
if db_url:
    if db_url.startswith("mysql://"):
        db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            echo=settings.DEBUG
        )
    elif db_url.startswith("sqlite"):
        # SQLite configuration for local development
        engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False},
            echo=settings.DEBUG
        )
    else:
        # Default configuration for other databases
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            echo=settings.DEBUG
        )
else:
    # Fallback to SQLite if no DATABASE_URL is provided
    print("⚠️  No DATABASE_URL found, using SQLite for local development")
    engine = create_engine(
        "sqlite:///./techkatta.db",
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for getting MySQL database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# MongoDB Database
class MongoDB:
    client: AsyncIOMotorClient = None
    
    def connect_db(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        
    def close_db(self):
        self.client.close()
        
    def get_database(self):
        return self.client[settings.MONGODB_DB_NAME]


mongodb = MongoDB()


async def get_mongo_db():
    """Dependency for getting MongoDB database"""
    return mongodb.get_database()
