from __future__ import annotations

from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy import Integer

from app.db.database import Base

class Wallet(Base):
	__tablename__ = "wallets"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	amount: Mapped[int] = mapped_column(NUMERIC(18, 2), nullable=False, default=0)