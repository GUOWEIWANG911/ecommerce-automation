# 1. 基础镜像：使用 Python 3.10 slim 版本，体积小且包含常用工具
FROM python:3.10-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 安装系统级依赖
# 必须安装 Chrome 浏览器和 ChromeDriver，否则 Selenium 无法运行
# libglib2.0-0 等库是 Chrome 运行必须的依赖
# 安装 wget, gnupg, 和 Chrome 所需的依赖库
RUN apt-get update && \
    apt-get install -y wget gnupg unzip libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libgdk-pixbuf2.0-0 libgtk-3-0 libx11-xcb1 libxcb-dri3-0 && \
    # 使用新的方式添加 Google 的 GPG 密钥
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg && \
    # 添加源列表，并指定使用刚才导入的密钥环
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    # 再次更新源列表并安装 Chrome
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    # 安装与当前 Chrome 版本匹配的 ChromeDriver
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) && \
    CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}" && \
    LATEST_VERSION=$(wget -qO- ${CHROMEDRIVER_URL}) && \
    wget -N https://chromedriver.storage.googleapis.com/${LATEST_VERSION}/chromedriver_linux64.zip -P /tmp && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver_linux64.zip && \
    # 清理缓存以减小镜像体积
    rm -rf /var/lib/apt/lists/*

# 4. 复制依赖文件并安装 Python 包
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 复制项目所有代码到容器中
COPY . .

# 6. 创建存放测试结果的目录
RUN mkdir -p /app/allure-results

# 7. 默认启动命令
# 如果 docker-compose.yml 中配置了 PYTEST_ADDOPTS，这里会被覆盖或追加
CMD ["pytest", "-v"]