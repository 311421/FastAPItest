from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context

from app.db.database import Base, DATABASE_URL
from app.models.wallet import Wallet  
target_metadata = Base.metadata

# Настройки логов Alembic
config = context.config
if config.config_file_name is not None:
	fileConfig(config.config_file_name)

# --- OFFLINE режим (генерация SQL без подключения)
def run_migrations_offline() -> None:
	url = DATABASE_URL
	context.configure(
		url=url,
		target_metadata=target_metadata,
		literal_binds=True,
		compare_type=True,
		compare_server_default=True,
	)
	with context.begin_transaction():
		context.run_migrations()

# --- ONLINE режим (подключение к БД)
from sqlalchemy.ext.asyncio import create_async_engine

def _run_migrations_in_connection(sync_connection) -> None:
    context.configure(
        connection=sync_connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(_run_migrations_in_connection)

def run_migrations_online() -> None:
	import asyncio
	asyncio.run(run_async_migrations())

if context.is_offline_mode():
	run_migrations_offline()
else:
	run_migrations_online()
