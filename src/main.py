import os
from fastapi import FastAPI, File, HTTPException, UploadFile, Response, status
from fastapi.responses import FileResponse
from src.config import Config
from src.posts.router import router as posts_router


app = FastAPI(docs_url="/api/docs")


app.include_router(posts_router)
