# src/alembic/env.py
from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context
from src.config import Settings

# Загружаем настройки
settings = Settings()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Подключаем метаданные моделей
from src.models import Base  # noqa: E402

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    config.set_main_option("sqlalchemy.url", settings.db_url)

    context.configure(
        url=settings.db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.db_url

    connectable = create_engine(
        settings.db_url,
        poolclass=pool.NullPool,
        echo=settings.echo,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=False,  # Если нет схем
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
