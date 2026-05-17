from typing import List, Any

from main.api.steps.admin_steps import AdminSteps
from main.api.steps.balance_steps import BalanceSteps
from main.api.steps.transfer_steps import TransferSteps
from main.api.steps.user_steps import UserSteps


class ApiManager:
    def __init__(self, created_obj: List[Any]):
        self.admin_steps = AdminSteps(created_obj)
        self.user_steps = UserSteps(created_obj)
        self.balance_steps = BalanceSteps(created_obj)
        self.transfer_steps = TransferSteps(created_obj)