from src.main.api.models.base_model import BaseModel


class DepositUserRequest(BaseModel):
    accountId: int
    amount: float
