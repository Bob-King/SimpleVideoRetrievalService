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
# text video_path
# There is a dog.   http://localhost:8000/files/1.mp4
python tools.py import_videos_from_csv <path_to_tsv>
```

# 测试服务

```bash
curl -X GET http://192.168.1.49:8000/api/v1/video -H "Content-Type: application/json" -d '{"text":"cat"}'
```