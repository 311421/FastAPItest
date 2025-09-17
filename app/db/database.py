from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:1234@localhost:5432/walletTest")

engine = create_async_engine(
	DATABASE_URL,
	echo=False,
	future=True,
)

async_session = async_sessionmaker(
	bind=engine,
	expire_on_commit=False,
	autoflush=False,
	autocommit=False,
)

async def get_session():
	async with async_session() as session:
		yield session

Base = declarative_base()



