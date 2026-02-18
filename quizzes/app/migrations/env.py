import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from db import Base
from models import *
from settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# sqlalchemy.engine.url.URL' returns a RFC-1738 quoted URL,
# which means that a password like "foo@" will be
# turned into "foo%40". This in turns causes a problem for
# set_main_option() because that uses ConfigParser.set, which (by
# design) uses python interpolation to write the string out
# where "%" is the special python interpolation character!
# Avoid this mismatch by quoting all %'s for the set below.

engine_url = settings.database_url.replace(
    '%', '%%'
)
print(engine_url)
config.set_main_option('sqlalchemy.url', engine_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # we use statement_cache_size=0 to work with pgbouncer in transaction mode
    # useful explanation about prepared statements, asyncpg, sql protocol, etc.
    # https://github.com/python-gino/gino/issues/80#issuecomment-337164497
    connect_args = {'statement_cache_size': 0, 'prepared_statement_cache_size': 0}

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
