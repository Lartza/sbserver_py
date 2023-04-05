from os import environ
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

env = environ.get('APPLICATION_ENV')
if env == 'production':
    DATABASE_URL = f"postgresql+asyncpg://sponsorblock:{environ['DB_PASSWORD']}@/sponsorblock?host=/run/postgresql"
elif env == 'test':
    DATABASE_URL = "sqlite+aiosqlite:///./test.db"
else:  # development
    DATABASE_URL = 'postgresql+asyncpg://sponsorblock@192.168.1.148/sponsorblock'

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
