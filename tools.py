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

            rsp = requests.post(
                url,
                json={"text": text, "video": video},
            )
            if rsp.status_code != HTTPStatus.OK:
                raise Exception(f"Failed to import video: {rsp.text}")


if __name__ == "__main__":
    fire.Fire({
        "import_videos_from_csv": import_videos_from_csv,
    })
