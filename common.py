from pydantic import BaseModel


class QueryVideoRequest(BaseModel):
    text: str
    similarity_threshold: float | None = 0.8
    topk: int | None = 3


class VideoInfo(BaseModel):
    video: str
    preview: str
    similarity: float


class PutVideoRequest(BaseModel):
    text: str
    video: str
    preview: str
