from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.crud_requester import CrudRequester
from main.api.foundation.requesters.validate_crud_requester import ValidateCRUDRequester
from main.api.models.transfer_user_request import TransferUserRequest
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.responce_specs import ResponseSpecs
from main.api.steps.base_steps import BaseSteps


class TransferSteps(BaseSteps):

    def transfer_user(self, transfer_user_request: TransferUserRequest, create_user_request):
        response = ValidateCRUDRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(transfer_user_request)

        return response

    def invalid_transfer_user(self, transfer_user_request: TransferUserRequest, create_user_request):
        CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_unprocessable()
        ).post(transfer_user_request)
