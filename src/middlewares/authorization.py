import typing

from strawberry.permission import BasePermission
from strawberry.types import Info


class RequestHeaderValidation(BasePermission):
    message = "Unauthorized request attempt. Missing required request header(s)."

    def has_permissions(self, source: typing.Any, info: Info, **kwargs) -> bool:
        return self.has_valid_enforced_headers(info.context["request"].headers)

    def has_valid_enforced_headers(self, headers: dict):
        """Check the value of the desired headers where applicable"""
        if headers["x-bookapi-token"]:
            return headers["x-bookapi-token"] == "fake-token-value123"
        else:
            return False
