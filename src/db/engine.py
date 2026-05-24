from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings

async_engine = create_async_engine(
    url=settings.db_url,
    pool_size=settings.pool_size,
    max_overflow=settings.max_overflow,
    pool_recycle=settings.pool_recycle,
    pool_pre_ping=settings.pool_pre_ping,
    echo=settings.echo,
)
