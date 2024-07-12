import functools
from typing import Any, Callable

from fastapi import HTTPException, Request

from src.config import Config


# class access_control:  # pylint: disable=invalid-name
#     def __init__(
#         cls,
#         open: bool = True,
#         superuser: bool = True,
#     ) -> None:
#         cls.superuser = superuser
#         cls.open: bool = open
#         cls.request: Request | None = None
#         cls.headers: dict[str, str] = None
#         cls.auth_header: str | None = None

#     def __call__(cls, function) -> Callable[..., Any]:
#         @functools.wraps(function)
#         async def decorated(*args, **kwargs):
#             try:
#                 await cls.parse_request(**kwargs)

#                 is_allowed = await cls.verify_request(*args, **kwargs)

#                 if not is_allowed:
#                     raise HTTPException(403, "Not allowed.")

#                 return await function(*args, **kwargs)

#             except Exception as error:
#                 raise HTTPException(403, str(error)) from error

#         return decorated

#     async def parse_request(cls, **kwargs) -> None:
#         pass

#     async def verify_request(cls, *args, **kwargs) -> bool:
#         """Actually check for permission based on route, user, tenant etc"""
#         print(args, kwargs)

#         return False