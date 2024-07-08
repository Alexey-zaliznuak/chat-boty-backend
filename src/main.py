from fastapi import APIRouter, FastAPI
from src.posts.router import router as posts_router


app = FastAPI(docs_url="/api/docs")


v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(posts_router)


app.include_router(v1_router)
