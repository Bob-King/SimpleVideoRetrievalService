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
* 运行服务
```bash
uvicorn app:app
```
