from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator
from app.core.config import settings

# MySQL Database
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
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
