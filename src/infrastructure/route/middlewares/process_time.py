from time import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time()

        response = await call_next(request)

        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time * 1000)) + " ms"

        return response
