
from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.validate_crud_requester import ValidateCRUDRequester
from main.api.models.create_user_request import CreateUserRequest, CreateCreditRequest
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.responce_specs import ResponseSpecs
from main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCRUDRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response
    def create_credit_account(self, create_credit_request: CreateCreditRequest):
        response = ValidateCRUDRequester(
            RequestSpecs.auth_headers(username=create_credit_request.username, password=create_credit_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response