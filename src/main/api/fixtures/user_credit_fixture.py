import pytest

from main.api.classes.api_manager import ApiManager
from main.api.models.create_user_request import CreateCreditRequest
from main.api.models.credit_repay_request import CreditRepayRequest
from main.api.models.credit_user_request import CreditUserRequest


@pytest.fixture
def create_credit(api_manager: ApiManager, create_credit_request: CreateCreditRequest, credit_amount: float,
                  credit_time: int):


    account = api_manager.user_steps.create_account(create_credit_request)
    credit_request = CreditUserRequest(
        accountId = account.id,
        amount = credit_amount,  # есть ошибка в требованиях
        termMonths = credit_time
    )
    credit_response = api_manager.balance_steps.credit_user(credit_request, create_credit_request)
    return {
        "account": account,
        "creditId": credit_response.creditId,
        "credit_response": credit_response,
        "amount": credit_response.amount
    }
@pytest.fixture
def credit_user_request(two_account_create, credit_amount, credit_time):
    account1, account2 = two_account_create
    return CreditUserRequest(
        accountId = account1.id,
        amount = credit_amount,
        termMonths = credit_time)
@pytest.fixture
def credit_repay_request(create_credit: CreditUserRequest):
    return CreditRepayRequest(
        creditId = create_credit["creditId"],
        accountId = create_credit["account"].id,
        amount = create_credit["amount"],
    )
@pytest.fixture
def incorrect_credit_repay_request(create_credit : CreditUserRequest, incorrect_repay: float):
    return CreditRepayRequest(
        creditId = create_credit["creditId"],
        accountId = create_credit["account"].id,
        amount = incorrect_repay
    )