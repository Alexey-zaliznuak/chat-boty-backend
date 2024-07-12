from typing import Any


from fastapi import HTTPException, Header, Security
from fastapi.security import APIKeyHeader
from src.config import Config


API_KEY = Config.AUTHORIZATION_KEY

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def authorization(api_key_header: str = Security(api_key_header)):
    if api_key_header != API_KEY:
        print(api_key_header)
        print()
        print(API_KEY, flush=True)

        raise HTTPException(status_code=403, detail="Forbidden")
