from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .engine import async_engine

async_session_factory = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
