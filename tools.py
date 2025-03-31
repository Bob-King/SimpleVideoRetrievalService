import csv
from http import HTTPStatus

import fire
import requests


def import_videos_from_csv(
        csv_file_path: str,
        delimiter: str = '\t',
        url: str = "http://localhost:8000/api/v1/video") -> None:
    with open(csv_file_path, mode='r', encoding='utf-8') as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter=delimiter)

        for row in reader:
            text = row.get('text')
            video = row.get('video')
            preview = row.get('preview')

            rsp = requests.post(
                url,
                json={"text": text, "video": video, "preview": preview}
            )
            if rsp.status_code != HTTPStatus.OK:
                raise Exception(f"Failed to import video: {rsp.text}")


def query_videos_by_text(
        text: str,
        similarity_threshold: float = 0.6,
        topk: int = 3,
        url: str = "http://localhost:8000/api/v1/video") -> None:
    rsp = requests.get(
        url,
        json={"text": text,
              "similarity_threshold": similarity_threshold, "topk": topk}
    )
    if rsp.status_code != HTTPStatus.OK:
        raise Exception(f"Failed to query videos: {rsp.text}")
    return rsp.text


if __name__ == "__main__":
    fire.Fire({
        "import_videos_from_csv": import_videos_from_csv,
        "query_videos_by_text": query_videos_by_text,
    })
