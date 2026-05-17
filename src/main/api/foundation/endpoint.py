from enum import Enum
from typing import Optional, Type

from dataclasses import dataclass

from main.api.models.create_account_response import CreateAccountResponse
from main.api.models.create_user_request import CreateUserRequest
from main.api.models.create_user_response import CreateUserResponse
from main.api.models.credit_repay_request import CreditRepayRequest
from main.api.models.credit_repay_response import CreditRepayResponse
from main.api.models.credit_user_response import CreditUserResponse
from main.api.models.credit_user_request import CreditUserRequest
from main.api.models.deposit_user_request import DepositUserRequest
from main.api.models.deposit_user_response import DepositUserResponse
from main.api.models.login_user_request import LoginUserRequest
from main.api.models.login_user_response import LoginUserResponse
from main.api.models.transfer_user_request import TransferUserRequest
from main.api.models.transfer_user_response import TransferUserResponse
from src.main.api.models.base_model import BaseModel

@dataclass
class EndpointConfiguration:
    url : str
    request_model : Optional[Type[BaseModel]]
    response_model : Optional[Type[BaseModel]]

class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model= CreateUserRequest,
        url= "/admin/create",
        response_model= CreateUserResponse
    )
    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model = None,
        url = "/admin/users",
        response_model = None
    )
    LOGIN_USER = EndpointConfiguration(
        request_model= LoginUserRequest,
        url= "/auth/token/login",
        response_model= LoginUserResponse
    )
    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        url="/account/create",
        response_model= CreateAccountResponse
    )
    DEPOSIT_ACCOUNT = EndpointConfiguration(
        request_model=DepositUserRequest,
        url="/account/deposit",
        response_model= DepositUserResponse

    )
    TRANSFER_ACCOUNT = EndpointConfiguration(
        request_model=TransferUserRequest,
        url="/account/transfer",
        response_model=TransferUserResponse
    )
    CREDIT_USER = EndpointConfiguration(
        request_model=CreditUserRequest,
        url="/credit/request",
        response_model=CreditUserResponse
    )
    CREDIT_REPAY = EndpointConfiguration(
        request_model=CreditRepayRequest,
        url="/credit/repay",
        response_model=CreditRepayResponse
    )



