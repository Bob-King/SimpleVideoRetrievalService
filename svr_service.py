import logging
import os
from http import HTTPStatus

import dashscope
import numpy as np

from common import VideoInfo


def compute_cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class SvrService:
    def __init__(self, db_path: str):
        self.db_path: str = db_path
        if os.path.exists(self.db_path):
            try:
                rdb = np.load(
                    db_path, allow_pickle=True).tolist()
                self.db: list[tuple[np.ndarray, str]] = [
                    (rdb["text_embeddings"][i],
                     rdb["videos"][i], rdb["previews"][i])
                    for i in range(len(rdb["text_embeddings"]))]
            except Exception as e:
                logging.error(f"Failed to load db: {e}")
                self.db: list[tuple[np.ndarray, str]] = []
        else:
            self.db: list[tuple[np.ndarray, str]] = []
        self.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

    def get_video(self, text: str, similarity_threshold: float,
                  topk: int) -> list[VideoInfo]:
        rsp = dashscope.TextEmbedding.call(
            model=dashscope.TextEmbedding.Models.text_embedding_v3,
            api_key=self.dashscope_api_key,
            input=text,
        )
        if rsp.status_code != HTTPStatus.OK:
            raise Exception("Failed to get text embedding")

        query_embedding = rsp["output"]["embeddings"][0]["embedding"]

        similarities = np.array([
            compute_cosine_similarity(embedding, query_embedding)
            for embedding, _, _ in self.db
        ])
        topk_indices = np.argsort(similarities)[::-1][:topk]
        topk_indices = topk_indices[similarities[topk_indices]
                                    > similarity_threshold]

        return [VideoInfo(video=self.db[i][1], preview=self.db[i][2],
                          similarity=similarities[i])
                for i in topk_indices]

    def put_video(self, text: str, video: str, preview: str) -> None:
        rsp = dashscope.TextEmbedding.call(
            model=dashscope.TextEmbedding.Models.text_embedding_v3,
            api_key=self.dashscope_api_key,
            input=text,
        )
        if rsp.status_code != HTTPStatus.OK:
            raise Exception("Failed to get text embedding")

        embedding = rsp["output"]["embeddings"][0]["embedding"]

        self.db.append((embedding, video, preview))
        np.save(self.db_path,
                {"text_embeddings": [row[0] for row in self.db],
                 "videos": [row[1] for row in self.db],
                 "previews": [row[2] for row in self.db]},
                allow_pickle=True)
