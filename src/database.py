import os
from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from dotenv import load_dotenv


load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'url_shortener')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_ECHO = os.getenv('DB_ECHO', 'True').lower() == 'true'

DATABASE_URL = (
    f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@'
    f'{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

engine = create_async_engine(DATABASE_URL, echo=DB_ECHO)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async dependency that yields SQLAlchemy async sessions
    """
    async with async_session_maker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

Base = declarative_base()
