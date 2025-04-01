import os
from typing import List, Optional

from fastapi import FastAPI,  Query
from fastapi.staticfiles import StaticFiles

from common import PutVideoRequest, VideoInfo
from svr_service import SvrService


app = FastAPI()
service = SvrService(db_path=os.environ.get(
    "DB_PATH", os.path.join("data", "db.npy")))

app.mount("/files", StaticFiles(directory=os.environ.get("FILES_DIR", "pub")))


@app.get("/api/v1/video")
async def get_video(
    text: str = Query(..., description="Query Text"),
    similarity_threshold: Optional[float] = Query(
        0.5, description="Similarity Threshold"),
    topk: Optional[int] = Query(3, description="Top K Results"),
) -> List[VideoInfo]:
    results = service.get_video(text, similarity_threshold, topk)
    return results


@app.post("/api/v1/video")
async def post_video(request: PutVideoRequest):
    service.put_video(request.text, request.video, request.preview)
