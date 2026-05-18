from xxlimited_35 import Null

import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.models.create_user_request import CreateUserRequest
from src.db.crud.account_crud import AccountCrudDB as Account


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, db_session: Session, api_manager: ApiManager,
                            create_user_request: CreateUserRequest):
        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance is not Null
        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'аккаунт не создан, счета нет в бд'
        assert account_from_db.balance is not None, 'Поле баланса отсутствует в бд '
