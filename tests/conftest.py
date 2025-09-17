import os
import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.database import Base, get_session as app_get_session

load_dotenv()
TEST_DB_URL = os.getenv("TEST_DATABASE_URL")

engine = create_async_engine(
	TEST_DB_URL,
	echo=False,
	future=True,
	poolclass=NullPool,
	pool_pre_ping=True,
)


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
	yield
	await engine.dispose()

@pytest.fixture
async def db_connection():
    async with engine.connect() as connection:
        trans = await connection.begin()
        try:
            yield connection
        finally:
            await trans.rollback()


@pytest.fixture
async def db_session(db_connection):
    SessionLocal = async_sessionmaker(
        bind=db_connection,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    )
    async with SessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession):
    async def override_get_session() -> AsyncSession:
        yield db_session

    app.dependency_overrides[app_get_session] = override_get_session
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()


