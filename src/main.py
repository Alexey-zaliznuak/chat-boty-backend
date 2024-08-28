from typing import Literal
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.infrastructure.route.middlewares import ProcessTimeMiddleware

from src.infrastructure.openapi import build_custom_openapi_schema
from src.infrastructure.rate_limit import limiter

from src.posts.router import router as posts_router
from src.cases.router import router as cases_router
from src.communication_requests.router import router as communication_requests_router


app = FastAPI(docs_url="/api/docs")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(posts_router)
v1_router.include_router(cases_router)
v1_router.include_router(communication_requests_router)


app.include_router(v1_router)


@app.get("/ping", response_model=Literal["pong"])
def ping():
    return {"message": "pong"}

app.openapi_schema = build_custom_openapi_schema(app)
