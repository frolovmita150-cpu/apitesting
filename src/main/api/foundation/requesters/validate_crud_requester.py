from typing import Optional

import allure

from main.api.configs.config import Config
from main.api.foundation.http_requster import HTTPRequester
from main.api.foundation.requesters.crud_requester import CrudRequester
from main.api.models.base_model import BaseModel


class ValidateCRUDRequester(HTTPRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: Optional[BaseModel] = None) -> Optional[BaseModel]:
        response = self.crud_requester.post(model)
        with allure.step(F"Post {Config.fetch("backendUrl")}{self.endpoint.value.url}"):
            allure.attach(F"Validate Model response: {self.endpoint.value.response_model.__name__}", )
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())
