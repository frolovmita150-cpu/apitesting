import pytest
from sqlalchemy.orm import Session
from main.api.classes.api_manager import ApiManager
from main.api.fixtures.kill_hardcode_numbers_fixture import deposit_amount
from main.api.models.create_user_request import CreateCreditRequest
from main.api.models.transfer_user_request import TransferUserRequest
from src.db.crud.transaction_crud import TransactionCrudDB as Transaction


@pytest.mark.api
@pytest.mark.transaction
class TestTransferMoney:
    def test_transfer_money(self, db_session: Session, api_manager: ApiManager,
                            transfer_money: TransferUserRequest, create_credit_request: CreateCreditRequest,
                            deposit_amount: float, transfer_balance: float):

        response = api_manager.transfer_steps.transfer_user(transfer_money, create_credit_request)
        assert response.fromAccountIdBalance == transfer_balance, 'Итоговый баланс не совпадает'

        transaction_from_db = Transaction.get_transaction_by_id(db_session, response.fromAccountId)
        assert transaction_from_db.from_account_id == response.fromAccountId, 'транзакция с id не найдена в бд '
        assert transaction_from_db.transaction_type == 'transfer', 'неверный тип у транзакции в бд '

    def test_transfer_invalid(self, api_manager: ApiManager, create_credit_request: CreateCreditRequest,
                              invalid_transfer_money: TransferUserRequest):

        response = api_manager.transfer_steps.invalid_transfer_user(invalid_transfer_money, create_credit_request)
        assert "error" in response.json(),'не зафиксирована ошибка в ответе '

