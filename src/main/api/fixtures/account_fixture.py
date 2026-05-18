import pytest

from main.api.classes.api_manager import ApiManager
from main.api.models.create_user_request import CreateUserRequest
from main.api.models.deposit_user_request import DepositUserRequest


# фикстура для подготовки данных для теста транзакции / делает и пополняет 1 аккаунт на полторы тысячи
# переделал под кредитного пользака что бы сразу можно было сделать негативную проверку
# не знаю насколько в рамках обучение критично потерять проверку о трансфере между счетами у обычного пользователя
@pytest.fixture
def two_account_create(api_manager : ApiManager, create_credit_request : CreateUserRequest, deposit_amount: float):
    account1 = api_manager.user_steps.create_account(create_credit_request)
    account2 = api_manager.user_steps.create_account(create_credit_request)
    deposit_request = DepositUserRequest(
        accountId = account1.id,
        amount = deposit_amount
    )
    api_manager.balance_steps.deposit_user(deposit_request, create_credit_request)
    account1.balance = deposit_request.amount
    return account1, account2
@pytest.fixture
def solo_account_create(api_manager : ApiManager, create_credit_request : CreateUserRequest, deposit_amount: float):
    account_depa = api_manager.user_steps.create_account(create_credit_request)
    return DepositUserRequest(
        accountId = account_depa.id,
        amount = deposit_amount
    )
