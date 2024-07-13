from fastapi import APIRouter, FastAPI

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.infrastructure.openapi import build_custom_openapi_schema
from src.infrastructure.rate_limit import limiter
from src.posts.router import router as posts_router


app = FastAPI(docs_url="/api/docs")


v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(posts_router)


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(v1_router)
app.openapi_schema = build_custom_openapi_schema(app)

