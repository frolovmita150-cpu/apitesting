import pytest

from main.api.models.credit_user_request import CreditUserRequest


@pytest.fixture
def create_credit(api_manager, create_credit_request):
    account = api_manager.user_steps.create_account(create_credit_request)
    credit_request = CreditUserRequest(
        accountId=account.id,
        amount=9000,  # есть ошибка в требованиях
        termMonths=16
    )
    credit_response = api_manager.balance_steps.credit_user(credit_request, create_credit_request)
    return {
        "account": account,
        "creditId": credit_response.creditId,
        "credit_response": credit_response,
        "amount": credit_response.amount
    }
