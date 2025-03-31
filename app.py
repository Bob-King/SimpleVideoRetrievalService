import os
from svr_service import SvrService

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from common import QueryVideoRequest, PutVideoRequest, VideoInfo


app = FastAPI()
service = SvrService(db_path=os.environ.get(
    "DB_PATH", os.path.join("data", "db.npy")))

app.mount("/files", StaticFiles(directory=os.environ.get("FILES_DIR", "pub")))


@app.get("/api/v1/video")
async def get_video(request: QueryVideoRequest) -> list[VideoInfo]:
    return service.get_video(request.text,
                             request.similarity_threshold, request.topk)


@app.post("/api/v1/video")
async def post_video(request: PutVideoRequest):
    service.put_video(request.text, request.video, request.preview)
