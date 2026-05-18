from random import randint, random
import pytest
@pytest.fixture
def credit_amount():
    return randint(5000, 14900)
@pytest.fixture
def credit_time():
    credit_time = randint(1, 18)
    return credit_time
@pytest.fixture
def incorrect_repay():
    return randint(14901, 15000)
@pytest.fixture
def deposit_amount():
    return randint(1000, 8000)
@pytest.fixture
def transfer_amount():
    return randint(500, 1000)
@pytest.fixture
def incorrect_transfer_amount():
    return randint(8100, 10000)
