from pydantic import BaseModel

class OperationResponse(BaseModel):
    status: str
    amount: int