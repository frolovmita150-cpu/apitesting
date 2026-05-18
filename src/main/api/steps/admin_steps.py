from main.api.foundation.endpoint import Endpoint
from main.api.foundation.requesters.crud_requester import CrudRequester
from main.api.foundation.requesters.validate_crud_requester import ValidateCRUDRequester
from main.api.models.create_user_request import CreateUserRequest
from main.api.models.login_user_request import LoginUserRequest
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.responce_specs import ResponseSpecs
from main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCRUDRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    def delete_user(self, user_id: int):
        CrudRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok()
        ).delete(user_id)

    def create_invalid_user(self, create_user_request: CreateUserRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(username='admin', password='123456'),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_bad()
        ).post(create_user_request)
        # === НАДЁЖНЫЙ ВЫВОД ===
        import json
        print("\n" + "═" * 70, flush=True)
        print(f"STATUS: {response.status_code}", flush=True)
        print(f"BODY:\n{response.text}", flush=True)

        try:
            print(f"JSON:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}", flush=True)
        except:
            pass
        print("═" * 70, flush=True)
        return response

    def login_user(self, login_user_request: LoginUserRequest):
        response = ValidateCRUDRequester(
            RequestSpecs.unauth_headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_ok()
        ).post(login_user_request)
        return response
