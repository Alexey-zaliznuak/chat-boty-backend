import os
from fastapi import FastAPI, File, HTTPException, UploadFile, Response, status
from fastapi.responses import FileResponse
from src.config import Config
from src.posts.router import router as posts_router


app = FastAPI(docs_url="/api/docs")


app.include_router(posts_router)

@app.post("/")
async def upload_index_page(file: UploadFile = File(...)):
    file_path = os.path.join(Config.STATIC_DIRECTORY, "index.html")

    os.makedirs(Config.STATIC_DIRECTORY, exist_ok=True)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/")
def get_index_page():
    path = os.path.join(Config.STATIC_DIRECTORY, "index.html")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=path, media_type='text/html')
