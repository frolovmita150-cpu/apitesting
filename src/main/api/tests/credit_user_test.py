import pytest
from sqlalchemy.orm import Session

from main.api.classes.api_manager import ApiManager
from main.api.models.create_user_request import CreateCreditRequest, CreateUserRequest
from main.api.models.credit_repay_request import CreditRepayRequest
from src.db.crud.credit_crud import CreditCrudDB as Credit
from src.db.crud.transaction_crud import TransactionCrudDB as Transaction


@pytest.mark.api
@pytest.mark.credit
class TestCreditUser:
    def test_credit_user(self, db_session: Session, api_manager: ApiManager,
                         create_credit_request: CreateCreditRequest, credit_user_request: CreateCreditRequest):

        response = api_manager.balance_steps.credit_user(credit_user_request, create_credit_request)
        assert credit_user_request.accountId == response.id  # там ошибка в свагере была((( только после отправки запроса с Accountid поменялось на id
        assert credit_user_request.termMonths == response.termMonths

        transaction_from_db = Transaction.get_credit_transaction_by_id(db_session, response.id)
        assert transaction_from_db.to_account_id == response.id, 'транзакция с id не найдена в бд '
        assert transaction_from_db.transaction_type == 'credit_issuance', 'неверный тип у транзакции в бд '

        credit_from_db = Credit.get_credit_by_id(db_session, response.id)
        assert credit_from_db.account_id == response.id, 'кредит у пользователя с id не найдена в бд '

    def test_credit_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest,
                            credit_user_request: CreateCreditRequest):
        # логин под пользаком без прав

        api_manager.balance_steps.invalid_credit_user(credit_user_request, create_user_request)

    def test_credit_repay(self, db_session: Session, api_manager: ApiManager,
                          create_credit_request: CreateCreditRequest, credit_repay_request: CreditRepayRequest ):
        # решил погашение сюда закинуть
        # возможно стоило в отдельные тесты
        response = api_manager.balance_steps.credit_repay(credit_repay_request, create_credit_request)
        assert credit_repay_request.creditId == response.creditId
        assert credit_repay_request.amount == response.amountDeposited

        transaction_from_db = Transaction.get_credit_repay_by_id(db_session, response.creditId)
        assert transaction_from_db.credit_id == response.creditId, 'транзакция с id не найдена в бд '
        assert transaction_from_db.transaction_type == 'credit_repayment', 'неверный тип у транзакции в бд '

        credit_from_db = Credit.get_credit_repay_by_id(db_session, response.creditId)
        assert credit_from_db.id == response.creditId, 'кредит у пользователя с id не найдена в бд '


    def test_credit_repay_invalid(self, api_manager: ApiManager, create_credit: CreateCreditRequest,
                                  create_credit_request: CreateCreditRequest,
                                  incorrect_credit_repay_request: CreditRepayRequest):

        api_manager.balance_steps.invalid_credit_repay(incorrect_credit_repay_request, create_credit_request)
