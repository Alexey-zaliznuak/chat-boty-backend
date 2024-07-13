from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def build_custom_openapi_schema(app: FastAPI):
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["ApiKeyAuth"] = {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }

    openapi_schema["security"] = [{"ApiKeyAuth": []}]

    return openapi_schema
