import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.fixtures.user_fixture import create_credit_request
from main.api.models.create_user_request import CreateUserRequest
from main.api.models.deposit_user_request import DepositUserRequest
from src.db.crud.account_crud import AccountCrudDB as Account


# позитивчик
@pytest.mark.api
@pytest.mark.deposit
class TestDeposit:

    def test_deposit_success(self, db_session: Session, api_manager: ApiManager,
                             create_credit_request: CreateUserRequest, solo_account_create: DepositUserRequest):
        response = api_manager.balance_steps.deposit_user(solo_account_create, create_credit_request)
        assert isinstance(response.id, int)
        balance_from_db = Account.get_account_by_id(db_session, response.id)
        assert balance_from_db.balance == response.balance, 'пополнение баланса отсутсвует в бд '

    @pytest.mark.parametrize(
        "amount",
        [999, 9001, 999.99, 9000.5, -500]  # корректно кушает str вместо float
        # либо я не учел и идет приведение типов
        # либо ошибка

    )
    def test_deposit_invalid(self, db_session: Session, api_manager: ApiManager,
                             amount:float,
                             create_credit_request: CreateUserRequest, solo_account_create: DepositUserRequest):
        solo_account_create.amount = amount
        response = api_manager.balance_steps.invalid_deposit_user(solo_account_create, create_credit_request)
        assert "error" in response.json(),'не зафиксирована ошибка в ответе '


