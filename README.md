# 环境搭建

目前只在windows平台做了测试

* 安装python 3.12
* 创建虚拟环境
```bash
cd <path_to_project_dir>
python -m venv .svrs
.\.svrs\Scripts\activate
pip install -r requirements.txt
```

# 运行服务

```bash
uvicorn app:app
```

# 添加数据

```bash
# tsv file format
# text video_path   preview
# There is a dog.   http://localhost:8000/files/1.mp4   http://localhost:8000/files/1.jpg
python tools.py import_videos_from_csv <path_to_tsv>
```

# 测试服务

```bash
curl -X GET http://localhost:8008/api/v1/video -H "Content-Type: application/json" -d '{"text":"cat","similarity_threshold":0.5,"topk":5}'
# [{"video":"http://localhost:8008/files/cat.mp4","preview":"http://localhost:8008/files/cat.jpg","similarity":0.6450275523998378}]

python tools.py query_videos_by_text 蓝天白云 --similarity_threshold 0.2 --url http://localhost:8008/api/v1/video
# [{"video":"http://localhost:8008/files/cat.mp4","preview":"http://localhost:8008/files/cat.jpg","similarity":0.40822904337325644},{"video":"http://localhost:8008/files/dog.mp4","preview":"http://localhost:8008/files/dog.jpg","similarity":0.3901900397589275}]
```