from fastapi import APIRouter
from app.schemas.request.wallet import OperationRequest, OperationType
from app.schemas.response.wallet import OperationResponse
from app.db.database import get_session
from app.services.wallet_operations import deposit_wallet, withdraw_wallet
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.services.wallet_operations import get_wallet

router = APIRouter()

@router.post("/v1/{wallet_uuid}/operation", response_model=OperationResponse)
async def deposit(wallet_uuid: int, body: OperationRequest, session: AsyncSession = Depends(get_session)) -> OperationResponse:
	match (body.operation_type):
		case OperationType.DEPOSIT:
			return await deposit_wallet(session, body, wallet_uuid)
		case OperationType.WITHDRAW:
			return await withdraw_wallet(session, body, wallet_uuid)

@router.get("/v1/wallets/{wallet_uuid}", response_model=OperationResponse)
async def get_wallet_route(wallet_uuid: int, session: AsyncSession = Depends(get_session)) -> OperationResponse:
	return await get_wallet(session, wallet_uuid)

