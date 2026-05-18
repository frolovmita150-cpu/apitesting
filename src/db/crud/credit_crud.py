from sqlalchemy.orm import Session

from src.db.models.credit_table import Credit


class CreditCrudDB:
    @staticmethod
    def get_credit_by_id(db: Session, id: int) -> Credit | None:
        return db.query(Credit).filter_by(account_id=id).first()

    def get_credit_repay_by_id(db: Session, credit_id: int) -> Credit | None:
        return db.query(Credit).filter_by(id=credit_id).first()
