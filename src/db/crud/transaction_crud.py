from sqlalchemy.orm import Session

from src.db.models.transfer_table import Transaction


class TransactionCrudDB:
    @staticmethod
    def get_transaction_by_id(db: Session, from_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=from_account_id).first()

    @staticmethod
    def get_credit_transaction_by_id(db: Session, id: int) -> Transaction | None:
        return (db.query(Transaction).filter_by(to_account_id=id, transaction_type='credit_issuance').first())

    @staticmethod
    def get_credit_repay_by_id(db: Session, credit_id: int) -> Transaction | None:
        return (db.query(Transaction).filter_by(credit_id=credit_id, transaction_type='credit_repayment').first())
    # сделал отдельный метод для проверки получения кредита в транзакции
    # так как она фикстура делает депозит перед кредитом тянет не тот запрос (с типом deposit)
