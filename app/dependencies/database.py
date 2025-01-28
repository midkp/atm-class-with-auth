from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Create the base class
Base = declarative_base()

# Your database URL, modify it for your actual database
DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Use this path for your SQLite DB

# Create the engine (make sure to use an async-compatible driver)
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create the sessionmaker for async sessions
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get the DB session
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Initialize database function
async def initialize_database():
    # Create all tables in the database (if not already created)
    async with engine.begin() as conn:
        # This will create all tables from models defined using Base
        await conn.run_sync(Base.metadata.create_all)
