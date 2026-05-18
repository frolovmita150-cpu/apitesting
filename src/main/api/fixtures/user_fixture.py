import pytest

from main.api.classes.api_manager import ApiManager
from main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest, CreateCreditRequest


@pytest.fixture
def create_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_credit_request(api_manager: ApiManager):  # вообще думал выделять отдельно модель и фикстуру под кредитного пользователя
    # решил что не стоит так как если ролей будет 10/20 сильно разрастется проект по файлам
    user_request = RandomModelGenerator.generate(CreateCreditRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request
