from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.Routers.wallet_router import router as wallet_router
from app.db.database import engine

app = FastAPI(title="Wallet API")

app.include_router(wallet_router, tags=["wallets"])