# 1. 基础镜像：使用 Python 3.10 slim 版本，体积小且包含常用工具
FROM python:3.10-slim

# 2. 设置工作目录
WORKDIR /app

# Playwright 需要一些基础系统库来运行浏览器，但不再需要手动安装 Chrome 和 ChromeDriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 4. 复制依赖文件并安装 Python 包
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 复制项目所有代码到容器中
COPY . .

# 6. 安装 Playwright 浏览器内核和系统依赖
# 这是最关键的一步，一条命令搞定所有浏览器和依赖，无需再手动管理驱动
RUN playwright install --with-deps chromium

# 7. 创建存放测试结果的目录
RUN mkdir -p /app/playwright-report /app/traces

# 8. 默认启动命令
CMD ["pytest", "-v"]