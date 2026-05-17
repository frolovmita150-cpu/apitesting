import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.models.transfer_user_request import TransferUserRequest
from src.db.crud.transaction_crud import TransactionCrudDB as Transaction


@pytest.mark.api
@pytest.mark.transaction
class TestTransferMoney:
    def test_transfer_money(self, db_session: Session, api_manager : ApiManager,
                            two_account_create, create_credit_request):
        account1, account2 = two_account_create
        transfer_request = TransferUserRequest(
            fromAccountId=account1.id,
            toAccountId=account2.id,
            amount=1200.75
        )
        response = api_manager.transfer_steps.transfer_user(transfer_request, create_credit_request)
        assert response.fromAccountIdBalance == (account1.balance - transfer_request.amount)
        assert transfer_request.toAccountId == response.toAccountId
        assert transfer_request.fromAccountId == response.fromAccountId
        transaction_from_db = Transaction.get_transaction_by_id(db_session, response.fromAccountId)
        assert transaction_from_db.from_account_id == response.fromAccountId, 'транзакция с id не найдена в бд '
        assert transaction_from_db is not None, 'транзакция отсутствует в бд'
        assert transaction_from_db.transaction_type == 'transfer', 'неверный тип у транзакции в бд '
        assert transaction_from_db.amount == transfer_request.amount, 'аляяярм сумма не совпадает, бабки улетают '

    def test_transfer_invalid(self, api_manager, two_account_create, create_credit_request):
        account1, account2 = two_account_create
        transfer_request = TransferUserRequest(
            fromAccountId=account1.id,
            toAccountId=account2.id,
            amount=5000
        )
        api_manager.transfer_steps.invalid_transfer_user(transfer_request, create_credit_request)

