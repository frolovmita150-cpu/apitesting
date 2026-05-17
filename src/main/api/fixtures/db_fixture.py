import pytest
from src.db.engine import SessionLocal,engine

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try :
        yield session
    finally:
        transaction.rollback()
        connection.close()