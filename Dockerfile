FROM python:3.10-slim

# 设置非root用户
RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app/uploads /app/output /app/temp && \
    chown -R appuser:appuser /app

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 切换运行时用户
USER appuser

# 设置环境变量
ENV DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}

CMD ["streamlit", "run", "web_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]