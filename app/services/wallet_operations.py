from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet
from app.schemas.response.wallet import OperationResponse
from app.schemas.request.wallet import OperationRequest
from fastapi import HTTPException

async def deposit_wallet(session: AsyncSession, body: OperationRequest, wallet_uuid: int) -> OperationResponse:
	if body.amount <= 0:
		raise HTTPException(status_code=400, detail="Deposit amount must be positive")

	query = select(Wallet).where(Wallet.id == wallet_uuid).with_for_update()
	res = await session.execute(query)
	wallet = res.scalar_one_or_none()
	if wallet is None:
		wallet = Wallet(id=wallet_uuid, amount=body.amount)
		session.add(wallet)
	else:
		wallet.amount = wallet.amount + body.amount

	await session.commit()
	return OperationResponse(status="success", amount=wallet.amount)

async def withdraw_wallet(session: AsyncSession, body: OperationRequest, wallet_uuid: int) -> OperationResponse:
	if body.amount <= 0:
		raise HTTPException(status_code=400, detail="Withdraw amount must be positive")

	query = select(Wallet).where(Wallet.id == wallet_uuid).with_for_update()
	res = await session.execute(query)
	wallet = res.scalar_one_or_none()
	if wallet is None:
		raise HTTPException(status_code=404, detail="Wallet not found")

	if wallet.amount < body.amount:
		raise HTTPException(status_code=400, detail="Insufficient balance")

	wallet.amount = wallet.amount - body.amount

	await session.commit()
	return OperationResponse(status="success", amount=wallet.amount)

async def get_wallet(session: AsyncSession, wallet_uuid: int) -> OperationResponse:
	query = select(Wallet).where(Wallet.id == wallet_uuid)
	res = await session.execute(query)
	wallet = res.scalar_one_or_none()
	if wallet is None:
		raise HTTPException(status_code=404, detail="Wallet not found")
	return OperationResponse(status="success", amount=wallet.amount)
    