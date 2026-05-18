from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.crud_requester import CrudRequester
from main.api.foundation.requesters.validate_crud_requester import ValidateCRUDRequester
from main.api.models.credit_repay_request import CreditRepayRequest
from main.api.models.credit_user_request import CreditUserRequest
from main.api.models.deposit_user_request import DepositUserRequest
from main.api.models.transfer_user_request import TransferUserRequest
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.responce_specs import ResponseSpecs
from main.api.steps.base_steps import BaseSteps


class BalanceSteps(BaseSteps):

    def deposit_user(self, deposit_user_request: DepositUserRequest, create_user_request):
        response = ValidateCRUDRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_user_request)

        return response

    def invalid_deposit_user(self, deposit_user_request: DepositUserRequest, create_user_request):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(deposit_user_request)
        return response

    # тоже подумал не выделять операции с балансов в отдельные степы
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

    def invalid_transer_user(self, transfer_user_request: TransferUserRequest, create_user_request):
        CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(transfer_user_request)

    # позитивны и негативный на работу с кредитом
    def credit_user(self, credit_user_request: CreditUserRequest, create_credit_request):
        response = ValidateCRUDRequester(
            RequestSpecs.auth_headers(
                username=create_credit_request.username,
                password=create_credit_request.password
            ),
            Endpoint.CREDIT_USER,
            ResponseSpecs.request_created()
        ).post(credit_user_request)

        return response

    def invalid_credit_user(self, credit_user_request: CreditUserRequest, create_credit_request):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_credit_request.username,
                password=create_credit_request.password
            ),
            Endpoint.CREDIT_USER,
            ResponseSpecs.request_forbidden()
        ).post(credit_user_request)
        return response

    def credit_repay(self, credit_repay_request: CreditRepayRequest, create_credit_request):
        response = ValidateCRUDRequester(
            RequestSpecs.auth_headers(
                username=create_credit_request.username,
                password=create_credit_request.password
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(credit_repay_request)
        return response

    def invalid_credit_repay(self, credit_repay_request: CreditRepayRequest, create_credit_request):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_credit_request.username,
                password=create_credit_request.password
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_unprocessable()
        ).post(credit_repay_request)
        return response