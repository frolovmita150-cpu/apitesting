import pytest

from main.api.classes.api_manager import ApiManager
from main.api.models.create_user_request import CreateUserRequest
from main.api.models.deposit_user_request import DepositUserRequest
from sqlalchemy.orm import Session
from src.db.crud.account_crud import AccountCrudDB as Account
# позитивчик
@pytest.mark.api
@pytest.mark.deposit
class TestDeposit:

    def test_deposit_success(self,db_session:Session, api_manager: ApiManager, create_user_request : CreateUserRequest):
        account = api_manager.user_steps.create_account(create_user_request)
        deposit_request = DepositUserRequest(
            accountId=account.id,
            amount=1500.75
        )
        response = api_manager.balance_steps.deposit_user(deposit_request, create_user_request)
        assert response.balance == deposit_request.amount
        assert isinstance(response.id, int)
        balance_from_db = Account.get_account_by_id(db_session, response.id)
        assert balance_from_db.balance == response.balance, 'пополнение баланса отсутсвует в бд '


    @pytest.mark.parametrize(
        "amount",
        [999, 9001, 999.99, 9000.5, -500] #корректно кушает str вместо float
        # либо я не учел и идет приведение типов
        # либо ошибка


    )


    def test_deposit_invalid(self, db_session:Session, api_manager: ApiManager, create_user_request : CreateUserRequest, amount):
        account = api_manager.user_steps.create_account(create_user_request)
        deposit_request = DepositUserRequest(
            accountId=account.id,
            amount=amount
        )
        api_manager.balance_steps.invalid_deposit_user(deposit_request, create_user_request)



