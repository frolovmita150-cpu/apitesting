import pytest

from main.api.models.credit_repay_request import CreditRepayRequest
from main.api.models.credit_user_request import CreditUserRequest
from src.db.crud.transaction_crud import TransactionCrudDB as Transaction
from src.db.crud.credit_crud import CreditCrudDB as Credit


@pytest.mark.api
@pytest.mark.credit
class TestCreditUser:
    def test_credit_user(self,db_session,api_manager, two_account_create, create_credit_request):
        account1, account2 = two_account_create
        credit_request = CreditUserRequest(
            accountId=account1.id,
            amount=9000, #есть ошибка в требованиях
            termMonths=16
        )
        response = api_manager.balance_steps.credit_user(credit_request, create_credit_request)
        assert credit_request.accountId == response.id #там ошибка в свагере была((( только после отправки запроса с Accountid поменялось на id
        assert credit_request.amount == response.amount
        assert credit_request.termMonths == response.termMonths
        assert credit_request.amount + account1.balance == response.balance

        transaction_from_db = Transaction.get_credit_transaction_by_id(db_session, response.id)
        assert transaction_from_db.to_account_id == response.id, 'транзакция с id не найдена в бд '
        assert transaction_from_db is not None, 'транзакция отсутствует в бд'
        assert transaction_from_db.transaction_type == 'credit_issuance', 'неверный тип у транзакции в бд '
        assert transaction_from_db.amount == credit_request.amount, 'аляяярм сумма не совпадает, бабки улетают '

        credit_from_db = Credit.get_credit_by_id(db_session, response.id)
        assert credit_from_db.account_id == response.id, 'кредит у пользователя с id не найдена в бд '
        assert credit_from_db.term_months == response.termMonths, 'срок кредита в бд отличается от отправленного в заявке'
        assert credit_from_db.amount == response.amount , 'сумма кредита отличается от нужной'
        assert credit_from_db.balance == response.amount * -1, 'баланс не бьется ПОЧЕМУ ТО'



    def test_credit_invalid(self,api_manager, two_account_create, create_user_request): #логин под пользаком без прав
        account1, account2 = two_account_create
        credit_request = CreditUserRequest(
            accountId=account1.id,
            amount=9000, #есть ошибка в требованиях
            termMonths=16
        )
        api_manager.balance_steps.invalid_credit_user(credit_request, create_user_request)

    def test_credit_repay(self,db_session, api_manager, create_credit, create_credit_request):#решил погашение сюда закинуть
        #возможно стоило в отддельные тесты
        repay_request = CreditRepayRequest(
            creditId=create_credit['creditId'],
            accountId=create_credit["account"].id,
            amount=create_credit["amount"]
        )
        response = api_manager.balance_steps.credit_repay(repay_request, create_credit_request)
        assert repay_request.creditId == response.creditId
        assert repay_request.amount == response.amountDeposited

        transaction_from_db = Transaction.get_credit_repay_by_id(db_session, response.creditId)
        assert transaction_from_db.credit_id == response.creditId, 'транзакция с id не найдена в бд '
        assert transaction_from_db is not None, 'транзакция отсутствует в бд'
        assert transaction_from_db.transaction_type == 'credit_repayment', 'неверный тип у транзакции в бд '
        assert transaction_from_db.amount == repay_request.amount, 'аляяярм сумма не совпадает, бабки улетают '

        credit_from_db = Credit.get_credit_repay_by_id(db_session, response.creditId)
        assert credit_from_db.id == response.creditId, 'кредит у пользователя с id не найдена в бд '
        assert credit_from_db.amount == response.amountDeposited, 'сумма кредита отличается от нужной'
        assert credit_from_db.balance == 0, 'баланс не бьется ПОЧЕМУ ТО'

    def test_credit_repay_invalid(self,api_manager, create_credit, create_credit_request):
        repay_request = CreditRepayRequest(
            creditId=create_credit['creditId'],
            accountId=create_credit["account"].id,
            amount=create_credit["amount"] + 1
        )
        api_manager.balance_steps.invalid_credit_repay(repay_request, create_credit_request)