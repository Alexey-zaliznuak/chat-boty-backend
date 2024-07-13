import functools
from typing import Any, Callable

from fastapi import HTTPException, Request
from starlette import status

from src.config import Config


class admin_access:  # pylint: disable=invalid-name
    def __init__(
        cls,
    ) -> None:
        cls.request: Request | None = None
        cls.auth_header: str | None = None

    def __call__(cls, function) -> Callable[..., Any]:
        @functools.wraps(function)
        async def decorated(*args, **kwargs):
            await cls.parse_request(**kwargs)

            is_allowed = await cls.verify_request()

            if not is_allowed:
                raise HTTPException(403, "Method not allowed.")

            return await function(*args, **kwargs)

        return decorated

    async def parse_request(cls, **kwargs) -> None:
        cls.request: Request = kwargs.get("request", None)

        if cls.request is None:
            raise ValueError("Request not provided")

        cls.auth_header = cls.request.headers.get("Authorization", None)

    async def verify_request(cls) -> bool:
        if cls.auth_header != Config.AUTHORIZATION_KEY:
            return False

        return True
