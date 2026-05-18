import pytest

from main.api.classes.api_manager import ApiManager
from main.api.models.create_user_request import CreateUserRequest, CreateCreditRequest
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username="admin", password="123456")

        response = api_manager.admin_steps.login_user(login_user_request)
        assert login_user_request.username == response.user.username, 'имя пользователя не совпадает'
        assert response.user.role == 'ROLE_ADMIN', 'роль пользователя не совпадает'

    def test_login_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username, 'имя пользователя не совпадает'
        assert response.user.role == 'ROLE_USER', 'роль пользователя не совпадает'

    def test_login_user_credit(self, api_manager: ApiManager, create_credit_request: CreateCreditRequest):
        response = api_manager.admin_steps.login_user(create_credit_request)

        assert create_credit_request.username == response.user.username, 'имя пользователя не совпадает'
        assert response.user.role == 'ROLE_CREDIT_SECRET', 'роль пользователя не совпадает'
