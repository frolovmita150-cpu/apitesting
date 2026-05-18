import pytest

from main.api.classes.api_manager import ApiManager
from main.api.fixtures.kill_hardcode_numbers_fixture import incorrect_transfer_amount
from main.api.models.create_user_request import CreateUserRequest
from main.api.models.deposit_user_request import DepositUserRequest
from main.api.models.transfer_user_request import TransferUserRequest

@pytest.fixture
def transfer_money(api_manager : ApiManager, create_credit_request : CreateUserRequest, deposit_amount: float,
                   transfer_amount: float, ):
    account1 = api_manager.user_steps.create_account(create_credit_request)
    account2 = api_manager.user_steps.create_account(create_credit_request)
    deposit_request = DepositUserRequest(
        accountId = account1.id,
        amount = deposit_amount
    )
    api_manager.balance_steps.deposit_user(deposit_request, create_credit_request)

    return  TransferUserRequest(
            fromAccountId = account1.id,
            toAccountId = account2.id,
            amount = transfer_amount
        )

@pytest.fixture
def invalid_transfer_money(api_manager : ApiManager, create_credit_request : CreateUserRequest, deposit_amount: float,
                   incorrect_transfer_amount: float, ):
    account1 = api_manager.user_steps.create_account(create_credit_request)
    account2 = api_manager.user_steps.create_account(create_credit_request)
    deposit_request = DepositUserRequest(
        accountId = account1.id,
        amount = deposit_amount
    )
    api_manager.balance_steps.deposit_user(deposit_request, create_credit_request)

    return  TransferUserRequest(
            fromAccountId = account1.id,
            toAccountId = account2.id,
            amount = incorrect_transfer_amount
        )

@pytest.fixture
def transfer_balance(deposit_amount: float, transfer_amount: float):
    itogi = deposit_amount - transfer_amount
    return itogi