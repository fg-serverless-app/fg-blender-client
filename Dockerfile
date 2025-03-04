# 使用官方Python镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用文件
COPY fastapi_server.py .
COPY index.html .

# 暴露端口
EXPOSE 8000

# 设置启动命令
CMD ["uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]